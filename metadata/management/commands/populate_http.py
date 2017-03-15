from importlib import import_module
from glob import glob

from django.core.management.base import BaseCommand, CommandError
from metadata.models import Tag
from ..logger import Logger

class Command(BaseCommand):
	help = 'Populate the Metadata and DataLocation for a dataset from Fits files on an HTTP server'
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The id of the dataset.')
		parser.add_argument('file_urls', nargs='+', metavar='file', help='URL to a fits file.')
		parser.add_argument('--update', default = False, action='store_true', help='Update metadata even if already present in DB')
		parser.add_argument('--tags', default = [], nargs='*', help='A list of tag names to set to the metadata')
		
	def handle(self, **options):
		
		log = Logger(self)
		
		# Import the record classes for the dataset
		try:
			records = import_module('metadata.management.records.' + options['dataset'])
			Record = records.RecordFromFitsFile
		except (ImportError, AttributeError):
			raise CommandError('No RecordFromFitsFile class for dataset %s' % options['dataset'])
		
		tags = list()
		for tag_name in options['tags']:
			tag, created = Tag.objects.get_or_create(name=tag_name)
			if created:
				log.info('Created Tag %s', tag_name)
			tags.append(tag)
		
		# Populate the dataset
		for file_url in args.file_urls:
			try:
				record = Record(file_url, log=log)
				record.save(tags=tags, update=options['update'])
			except Exception, why:
				log.error('Error creating record for "%s": %s', file_url, why)
