from datetime import datetime
from dateutil.parser import parse as parse_date
from importlib import import_module
from django.core.management.base import BaseCommand, CommandError
from _logger import Logger

class Command(BaseCommand):
	help = 'Populate the Metada and DataLocation for a dataset'
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The id of the dataset.')
		parser.add_argument('start_date', type = lambda s: parse_date(s), help='The start date.')
		parser.add_argument('end_date', nargs = '?', type = lambda s: parse_date(s), default = datetime.utcnow(), help='The end date.')
		parser.add_argument('--update', default = False, action='store_true', help='Update metadata even if already present in DB')
		
	def handle(self, **options):
		# Import the populate module for the dataset and call it's populate function
		try:
			populate = import_module(options['dataset'] + '.tools.populate')
			populate.populate(options['start_date'], options['end_date'], options['update'], Logger(self))
		except Exception, why:
			raise CommandError('Cannot populate dataset %s: %s' % (options['dataset'], why))