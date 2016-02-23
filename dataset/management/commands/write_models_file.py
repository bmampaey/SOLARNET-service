from django.core.management.base import BaseCommand, CommandError
from ..logger import Logger

from dataset.models import Dataset, Keyword

models_header = '''
from __future__ import unicode_literals
from django.db import models
from dataset.models import BaseMetadata

class Metadata(BaseMetadata):
'''

field_template = '\t{keyword.db_column} = {field_type}(\'{keyword.name}\', help_text=\'{keyword.description}\', blank=True, null=True)'

def field_for_type(python_type):
	if python_type == 'str':
		return 'models.TextField'
	elif python_type == 'datetime':
		return 'models.DateTimeField'
	elif python_type == 'int':
		return 'models.IntegerField'
	elif python_type == 'float':
		return 'models.FloatField'
	elif python_type == 'bool':
		return 'models.NullBooleanField'
	else:
		raise CommandError('Unknown model field type for python type %s' % python_type)


class Command(BaseCommand):
	help = 'Generate the models file for a dataset. Writes to output.'
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The id of the dataset.')
		
	def handle(self, **options):
		# Create a logger
		log = Logger(self)
		
		# Get the dataset
		try:
			dataset = Dataset.objects.get(id = options['dataset'])
		except Dataset.DoesNotExist:
			raise CommandError('Dataset %s does not exists in the dataset table' % options['dataset'])
		
		# Get the keywords for the dataset
		keywords = Keyword.objects.filter(dataset = dataset)
		
		print models_header,
		if keywords.exists():
			for keyword in keywords:
				if keyword.db_column in ['id', 'oid', 'fits_header', 'data_location', 'tags']:
					raise CommandError('Keywords %s is duplicate of existing keyword in BaseMetadata' % keyword.db_column)
				elif keyword.db_column not in ['date_beg', 'date_end', 'wavemin', 'wavemax']:
					print field_template.format(keyword = keyword, field_type = field_for_type(keyword.python_type))
		else:
			print '\tpass'
