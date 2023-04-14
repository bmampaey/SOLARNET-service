import json
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import transaction

from project.utils import Logger
from dataset.models import Dataset, Keyword


class Command(BaseCommand):
	help = 'Output the keywords in JSON format as generated by the script extract_keywords_from_fits'
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The name of the dataset')
	
	def handle(self, **options):
		# Create a logger
		self.log = Logger(self, options.get('verbosity', 2))
		
		# Get the dataset
		try:
			dataset = Dataset.objects.get(name = options['dataset'])
		except Dataset.DoesNotExist:
			raise CommandError('Dataset %s not found' % options['dataset'])
		
		print(json.dumps(self.get_keyword_infos(dataset), indent='\t'))
	
	
	def get_keyword_infos(self, dataset):
		'''Return a list of all keyword info {name, verbose_name, type, unit, description}'''
		
		keyword_infos = list()
		
		for keyword in dataset.keywords.exclude(name__in = ['id']):
			
			keyword_infos.append({
				'name': keyword.name,
				'verbose_name': keyword.verbose_name,
				'type': keyword.type,
				'unit': keyword.unit,
				'description': keyword.description,
			})
		
		return keyword_infos
