from datetime import datetime
from dateutil.parser import parse as parse_date
#from importlib import import_module
from django.core.management.base import BaseCommand, CommandError
import ..populate
from ..logger import Logger

class Command(BaseCommand):
	help = 'Populate the Metadata and DataLocation for a dataset'
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The id of the dataset.')
		parser.add_argument('files', nargs='+', metavar='file', help='Path to a fits file.')
		parser.add_argument('--update', default = False, action='store_true', help='Update metadata even if already present in DB')
		
	def handle(self, **options):
		
		log = Logger(self)
		
		# Check if the dataset has a specific populator
		try:
			populate = import_module(options['dataset'] + '.management.populate')
		except ImportError:
			log.warning('No Populator for dataset %s, using generic Populator', options['dataset'])
		
		# Create a populator for the dataset
		try
			populator = populate.Populator(options, log=log)
		except Exception, why:
			raise CommandError('Could not create Populator for dataset %s: %s', options['dataset'])
		
		# Glob the file paths
		file_paths = list()
		for path in options['files']:
			files.extend(glob(path))
		
		# Populate the dataset
		for file_path in file_paths:
			try:
				populator.populate(file_path, update=options['update'])
			except Exception, why:
				log.error('Error creating record for "%s": %s', file_path, why)


