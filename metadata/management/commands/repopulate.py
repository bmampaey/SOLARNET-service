from importlib import import_module

from django.core.management.base import BaseCommand, CommandError
from ..logger import Logger

class Command(BaseCommand):
	help = 'Repopulate the Metadata from the fits_header field '
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The id of the dataset.')
		parser.add_argument('oids', nargs='*', metavar='OID', help='OID to reparse, all if not specified.')
		parser.add_argument('--debug', default = False, action='store_true', help='Show debugging info')
		
	def handle(self, **options):
		
		log = Logger(self, debug=options['debug'])
		
		# Import the record classes for the dataset
		try:
			records = import_module('metadata.management.records.' + options['dataset'])
			Record = records.Record
		except (ImportError, AttributeError):
			raise CommandError('No Record class for dataset %s' % options['dataset'])
		
		# Get the list of metadata to repopulate
		if options['oids']:
			metadata_list = Record.metadata_model.objects.filter(oid__in=options['oids']).iterator()
		else:
			metadata_list = Record.metadata_model.objects.iterator()
		
		# Repopulate the dataset
		for metadata in metadata_list:
			try:
				Record.update(metadata)
			except Exception, why:
				log.error('Error resaving record for "%s": %s', metadata, why)

