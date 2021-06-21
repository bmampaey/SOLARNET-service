from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from importlib import import_module
from glob import glob

from django.core.management.base import BaseCommand, CommandError
from sunpy.net import vso
from metadata.models import Tag
from ..logger import Logger

class Command(BaseCommand):
	help = 'Populate the Metadata and DataLocation for a dataset from VSO records'
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The id of the dataset')
		parser.add_argument('start_date', type = lambda s: parse_date(s), help='The start date')
		parser.add_argument('end_date', nargs = '?', type = lambda s: parse_date(s), default = datetime.utcnow(), help='The end date')
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
		
		# Populate the dataset
		for vso_record in vso_records(Record.instrument, options['start_date'], options['end_date']):
			try:
				record = Record(vso_record, log=log)
				record.create(tags=tags, update=options['update'])
			except Exception as why:
				log.error('Error creating record for "%s": %s', vso_record.fileid, why)


def vso_records(instrument, start_date, end_date, time_increment = timedelta(hours=1)):
	'''Generator that fetch and returns the VSO records'''
	# We use the sunpy VSO client to get the VSO records
	client = vso.VSOClient()
	while start_date <= end_date:
		for record in client.query_legacy(start_date, min(start_date + time_increment, end_date), instrument=instrument):
			yield record
		start_date += time_increment
 