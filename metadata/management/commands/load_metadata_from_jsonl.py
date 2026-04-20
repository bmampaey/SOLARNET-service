import json

from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.python import Deserializer
from django.db import transaction

from dataset.models import DataLocation, Dataset
from project.utils import Logger


class Command(BaseCommand):
	help = 'Load the metadata from a JSONL (JSON Lines) file'

	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The name of the dataset')
		parser.add_argument('file_path', metavar='JSONL-FILE', help='The path to the JSONL file')
		parser.add_argument('--continue-on-fail', '-c', action='store_true', help='If a row fails to save, continue')

	def handle(self, **options):
		# Create a logger
		self.log = Logger(self, options.get('verbosity', 2))

		# Get the dataset
		try:
			dataset = Dataset.objects.get(name=options['dataset'])
		except Dataset.DoesNotExist:
			raise CommandError('Dataset %s not found' % options['dataset'])

		metadata_model_name = '{meta.app_label}.{meta.model_name}'.format(meta=dataset.metadata_model._meta)
		datalocation_model_name = '{meta.app_label}.{meta.model_name}'.format(meta=DataLocation._meta)

		with open(options['file_path']) as file:
			with transaction.atomic():
				for line_number, line in enumerate(file, start=1):
					metadata = json.loads(line)
					# Setting all the forign keys is normally done by the RestFull API
					# So we have to do it manually
					data_location = metadata.pop('data_location')
					metadata.setdefault('data_location', (dataset.natural_key(), data_location['file_url']))
					data_location.setdefault('dataset', dataset.natural_key())

					# Use the python Deserializer dunction instead of the json onse so we don't have to re-encode to JSON first
					# The order is important
					try:
						for deserialized in Deserializer([
							{'model': datalocation_model_name, 'fields': data_location},
							{'model': metadata_model_name, 'fields': metadata},
						]):
							# Altough desiarilized has a save method, it bypasses the normal Model save() methos, and the update_time of DataLocation is now poupulated with the current time
							deserialized.object.save()
							self.log.info('Saved object %s', deserialized.object)
					except Exception as error:
						if options['continue_on_fail']:
							self.log.warning('Could not save metadata line %s: %s. Continuing!', line_number, error)
							continue
						else:
							raise CommandError('Could not save metadata line %s: %s!', line_number, error) from error
