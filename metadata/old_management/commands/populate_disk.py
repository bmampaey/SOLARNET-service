from importlib import import_module
from glob import glob

from django.core.management.base import BaseCommand, CommandError
from metadata.models import Tag
from ..logger import Logger

class Command(BaseCommand):
	help = 'Populate the Metadata and DataLocation for a dataset from Fits files on disk'
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The id of the dataset')
		parser.add_argument('files', nargs='+', metavar='file', help='Path to a fits file')
		parser.add_argument('--HDU', type=int, help='The HDU of the fits file to read')
		parser.add_argument('--update', default = False, action='store_true', help='Update metadata even if already present in DB')
		parser.add_argument('--tags', default = [], nargs='*', help='A list of tag names to set to the metadata')
		parser.add_argument('--debug', default = False, action='store_true', help='Show debugging info')
		
	def handle(self, **options):
		
		log = Logger(self, debug=options['debug'])
		
		# Import the record classes for the dataset
		try:
			records = import_module('metadata.management.records.' + options['dataset'])
			Record = records.Record
		except (ImportError, AttributeError):
			raise CommandError('No Record class for dataset %s' % options['dataset'])
		
		tags = list()
		for tag_name in options['tags']:
			tag, created = Tag.objects.get_or_create(name=tag_name)
			if created:
				log.info('Created Tag %s', tag_name)
			tags.append(tag)
		
		# Glob the file paths
		file_paths = list()
		for path in options['files']:
			file_paths.extend(glob(path))
		file_paths.sort()
		
		# Populate the dataset
		for file_path in file_paths:
			try:
				record = Record(file_path, hdu = options['HDU'], log=log)
				record.create(tags=tags, update=options['update'])
			except Exception as why:
				log.error('Error creating record for "%s": %s', file_path, why)
