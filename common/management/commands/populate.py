from datetime import datetime
from dateutil.parser import parse as parse_date
from importlib import import_module
from django.core.management.base import BaseCommand, CommandError
from _logger import Logger

class Command(BaseCommand):
	help = 'Populate the Metada and DataLocation for a data series'
	
	def add_arguments(self, parser):
		parser.add_argument('data_series', help='The id of the data series.')
		parser.add_argument('start_date', type = lambda s: parse_date(s), help='The start date.')
		parser.add_argument('end_date', nargs = '?', type = lambda s: parse_date(s), default = datetime.utcnow(), help='The end date.')
		parser.add_argument('--update', default = False, action='store_true', help='Update metadata even if already present in DB')
		
	def handle(self, **options):
		# Import the populate module for the data series and call it's populate function
		try:
			populate = import_module(options['data_series'] + '.tools.populate')
			populate.populate(options['start_date'], options['end_date'], options['update'], Logger(self))
		except Exception, why:
			raise CommandError('Cannot populate data series %s: %s' % (options['data_series'], why))