from datetime import datetime
import dateutil.parser
import re
from collections import defaultdict
import pyfits

from _logger import Logger

def column_name(key):
	'''Transform a keyword into an acceptable column name'''
	# It is more simpler in postgres to have column names in lower case and without spaces
	return re.sub("\W", "_", key.strip()).lower()

def value_type(value):
	'''Return the string representation of the type'''
	if isinstance(value, float):
		return "float"
	elif isinstance(value, (int, long)):
		return "int"
	elif isinstance(value, datetime):
		return "datetime"
	elif isinstance(value, bool):
		return "bool"
	else:
		return "str"

unit_pattern =  re.compile(r"\s*(\[\s*(?P<unit>[^\]]*)\s*\])?(?P<comment>.*)\s*")
def extract_unit(comment):
	'''Split the unit from the comment'''
	# Units are usually specified at the beginning of the comment between brackets
	try:
		parts = unit_pattern.match(comment).groupdict()
	except Exception:
		return "", comment.strip()
	else:
		return parts["unit"].strip() if parts["unit"] is not None else "", parts["comment"].strip()


def get_keywords(header, excluded = [], log):
	'''Extract the keywords information from the header'''
	
	keywords = list()
	comment_index = 0
	history_index = 0
	
	for card in header:
		try:
			key = card.key
			value = card.value
			comment = card.comment
		except Exception, why:
			log.error("Could not parse card %s: %s. Skipping.", card, why)
			continue
		
		if key.upper() in excluded:
			log.info('Skipping excluded keyword %s', key)
			continue
		
		elif key.lower() == "history":
			value.strip(" \t\n-")
			if not value:
				# We omit empty history
				continue	
			# history keywords are not unique
			db_column = "history_%d" % history_index
			history_index += 1
		
		
		elif key.lower() == "comment":
			value.strip(" \t\n-")
			if not value:
				# We omit empty comment
				continue	
			# comment keywords are not unique
			db_column = "comment_%d" % comment_index
			comment_index += 1
		
		else:
			db_column = column_name(key)
		
		python_type = value_type(value)
		unit, description = extract_unit(comment)
		
		keywords.append({
			'key': key,
			'db_column': db_column,
			'python_type': python_type,
			'unit': unit,
			'description': description
		})
	
	return keywords


class Command(BaseCommand):
	help = 'Inspect the fits_header field of a dataset Metadata and extract the keywords definition'
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The id of the dataset.')
		parser.add_argument('--comments', '-C', default=False, action='store_true', help='Extract pure comment keywords')
		parser.add_argument('--history', '-H', default=False, action='store_true', help='Extract history keywords')
		parser.add_argument('--exclude', '-E', default = ["DATASUM", "CHECKSUM", "SIMPLE", "BITPIX"], nargs='*', help='Keywords to exclude (in small caps)')
		
	def handle(self, **options):
		# Parse the options
		excluded = map(lambda s: s.upper(), options['exclude'])
		if not options['comments']:
			excluded.append('COMMENT')
		if not options['history']:
			excluded.append('HISTORY')
		import pdb; pdb.set_trace()
		# Import the dataset models
		try:
			models = import_module(options['dataset'] + '.models')
		except Exception, why:
			raise CommandError('Cannot import %s models: %s' % (options['dataset'], why))
		
		# As keywords can be different from one fits file to another
		# We collect all the possible info variation 
		all_keywords = defaultdict(lambda : defaultdict(set))
		
		for metadata in models.Metadata.objects.all():
			# Reconstruct header from the metadata fits_header field
			header = pyfits.Header.fromstring(metadata.fits_header)
			# Extract the keywords and update the complete list
			keywords = get_keywords(header, excluded, Logger(self))
			for keyword in keywords:
				for info, value in keyword.iteritems():
					all_keywords[keyword['key']][info].add(value)
