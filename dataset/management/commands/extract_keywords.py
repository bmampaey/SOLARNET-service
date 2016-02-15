from datetime import datetime
from dateutil.parser import parse as parse_date
import re
from collections import defaultdict, Counter
import pickle
from django.core.management.base import BaseCommand, CommandError
import pyfits

from ..logger import Logger
from dataset.models import Dataset, Keyword

def column_name(keyword):
	'''Transform a keyword into an acceptable column name'''
	# It is more simpler in postgres to have column names in lower case and without spaces
	return re.sub('\W', '_', keyword.strip()).lower()

def value_type(value):
	'''Return the string representation of the type'''
	if isinstance(value, float):
		return 'float'
	elif isinstance(value, (int, long)):
		return 'int'
	elif isinstance(value, datetime):
		return 'datetime'
	elif isinstance(value, bool):
		return 'bool'
	else:
		try:
			parse_date(value)
		except Exception:
			return 'str'
		else:
			return 'datetime'


unit_pattern =  re.compile(r'\s*(\[\s*(?P<unit>[^\]]*)\s*\])?(?P<comment>.*)\s*')
def extract_unit(comment):
	'''Split the unit from the comment'''
	# Units are usually specified at the beginning of the comment between brackets
	try:
		parts = unit_pattern.match(comment).groupdict()
	except Exception:
		return '', comment.strip()
	else:
		return parts['unit'].strip() if parts['unit'] is not None else '', parts['comment'].strip()


def get_keywords(header, log, excluded = []):
	'''Extract the keywords information from the header'''
	
	keywords = list()
	comment_index = 0
	history_index = 0
	
	for card in header.cards:
		try:
			keyword = card.keyword
			value = card.value
			comment = card.comment
		except Exception, why:
			log.error('Could not parse card %s: %s. Skipping.', card, why)
			continue
		
		if keyword.upper() in excluded:
			log.debug('Skipping excluded keyword %s', keyword)
			continue
		
		elif keyword.upper() == 'HISTORY':
			value.strip(' \t\n-')
			if not value:
				# We omit empty history
				continue	
			# history keywords are not unique
			db_column = 'history_%d' % history_index
			history_index += 1
		
		
		elif keyword.upper() == 'COMMENT':
			value.strip(' \t\n-')
			if not value:
				# We omit empty comment
				continue	
			# comment keywords are not unique
			db_column = 'comment_%d' % comment_index
			comment_index += 1
		
		else:
			db_column = column_name(keyword)
		
		python_type = value_type(value)
		unit, description = extract_unit(comment)
		
		keywords.append({
			'name': keyword,
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
		parser.add_argument('--max_record', '-m', type = int, default = None, help='Maximum number of record to inspect')
		parser.add_argument('--comments', '-C', default=False, action='store_true', help='Extract pure comment keywords')
		parser.add_argument('--history', '-H', default=False, action='store_true', help='Extract history keywords')
		parser.add_argument('--exclude', '-E', default = ['DATASUM', 'CHECKSUM', 'SIMPLE', 'BITPIX'], nargs='*', help='keywords to exclude (in small caps)')
		parser.add_argument('--no_backup', '-b', default=False, action='store_true', help='Do not write backup after parsing has finished')
		
	def handle(self, **options):
		# Parse the options
		excluded = map(lambda s: s.upper(), options['exclude'])
		if not options['comments']:
			excluded.append('COMMENT')
		if not options['history']:
			excluded.append('HISTORY')
		
		# Create a logger
		log = Logger(self)
		
		# Get the dataset
		try:
			dataset = Dataset.objects.get(id = options['dataset'])
		except Dataset.DoesNotExist:
			raise CommandError('Dataset %s does not exists in the dataset table' % options['dataset'])
		
		# Get the dataset Metadata model
		try:
			Metadata = dataset.metadata_model
		except Exception, why:
			raise CommandError('Cannot import %s Metadata model: %s' % (options['dataset'], why))
		
		# Get the metadata to inspect
		if options['max_record']:
			# If there is a max records we take them at random
			metadatas = Metadata.objects.order_by('?')[:options['max_record']]
		else:
			# If the number of records is unlimited, we need to use iterator()) instead of all(), because there can be too many records to fit in memory
			metadatas = Metadata.objects.iterator()
		
		# As keywords can be different from one fits file to another
		# We count all the possible info variation values
		all_keywords = defaultdict(lambda : defaultdict(Counter))
		
		# Extract the keywords and update the list of all keywords
		for metadata in metadatas:
			log.info(str(metadata.oid))
			# Reconstruct header from the metadata fits_header field
			header = pyfits.Header.fromstring(metadata.fits_header)
			
			keywords = get_keywords(header, log, excluded)
			for keyword in keywords:
				for info, value in keyword.iteritems():
					all_keywords[keyword['name']][info][value] += 1
		
		# Write a backup of all keywords in case of problem
		if not options['no_backup']:
			backup_filename = options['dataset'] + '_keywords.pickle'
			try:
				with open(backup_filename, 'w') as f:
					pickle.dump(all_keywords, f, pickle.HIGHEST_PROTOCOL)
			except Exception, why:
				log.error('Could not write backup file %s: %s', backup_filename, why)
		
		
		# Ask user to select between possible info values if there is more than one
		for keyword, infos in all_keywords.iteritems():
			for info, values in infos.iteritems():
				if len(values) > 1:
					selections = values.most_common()
					total = sum(values.values())
					while True:
						print 'Please select best option for keyword',  keyword, info, ':'
						for i, (value, count) in enumerate(selections):
							print '{i}. {v} [{c}/{t}]'.format(i=i, v=value, c=count, t = total)
						selection = raw_input('option number: ')
						if selection.isdigit() and int(selection) < len(selections):
							infos[info] = selections[int(selection)][0]
							break
						else:
							print 'Invalid selection', selection
				else:
					infos[info] = values.most_common(1)[0][0]
		
		# Insert the keyword info into the DB
		for keyword, infos in all_keywords.iteritems():
			obj, created = Keyword.objects.get_or_create(dataset = dataset, name = keyword, defaults = infos)
			if created:
				log.info('Created keyword %s with info %s', keyword, infos)
			else:
				log.warning('Keyword %s already exists', keyword)
				for info, value in infos.iteritems():
					if getattr(obj, info) != value:
						log.error('%s differ from existing (%s) to extracted (%s)', info, getattr(obj, info), value)