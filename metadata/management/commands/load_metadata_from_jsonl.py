import json
from datetime import datetime, timezone

from django.core.management.base import BaseCommand, CommandError
from django.db import models, transaction
from django.utils.timezone import is_naive, make_aware, utc

from dataset.models import DataLocation, Dataset
from project.utils import Logger


class Command(BaseCommand):
	help = 'Load the metadata from a JSONL (JSON Lines) file'

	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The name of the dataset')
		parser.add_argument('file_path', metavar='JSONL-FILE', help='The path to the JSONL file')
		parser.add_argument('--continue-on-fail', '-c', action='store_true', help='If a row fails to save, continue')
		parser.add_argument('--batch-size', '-b', type=int, default=1000, help='Number of rows to save')

	def handle(self, **options):
		# Create a logger
		self.log = Logger(self, options.get('verbosity', 2))

		# Get the dataset
		try:
			self.dataset = Dataset.objects.get(name=options['dataset'])
		except Dataset.DoesNotExist:
			raise CommandError('Dataset %s not found' % options['dataset'])

		MetaData = self.dataset.metadata_model
		now_utc = datetime.now(timezone.utc)

		metadatas = {}
		data_locations = {}
		first_line_number = 1

		with open(options['file_path']) as file:
			for line_number, line in enumerate(file, start=1):
				metadata = json.loads(line)
				data_location = metadata.pop('data_location')
				metadatas[data_location['file_url']] = self.make_timezone_aware(MetaData(**metadata))
				data_locations[data_location['file_url']] = DataLocation(dataset=self.dataset, update_time=now_utc, **data_location)

				if len(data_locations) >= options['batch_size']:
					try:
						self.save_objects(data_locations, metadatas, continue_on_fail=options['continue_on_fail'])
						self.log.info('Saved objects from line %s to line %s', first_line_number, line_number)
						first_line_number = line_number + 1
						metadatas = {}
						data_locations = {}
					except Exception as error:
						raise CommandError(
							'Error saving objects between line %s and %s: %s!' % (first_line_number, line_number, error)
						) from error

		if data_locations:
			try:
				self.save_objects(data_locations, metadatas, continue_on_fail=options['continue_on_fail'])
				self.log.info('Saved objects from line %s to line %s', first_line_number, line_number)
			except Exception as error:
				raise CommandError(
					'Error saving objects between line %s and %s: %s!' % (first_line_number, line_number, error)
				) from error

		self.log.info('Finnished loading all %s lines', line_number)

	def make_timezone_aware(self, object, default_timezone=utc):
		"""Make sure that the times have a timezone set"""
		for field in object._meta.get_fields():
			# Check if the field is a DateTimeField (ignores DateField or TimeField)
			if isinstance(field, models.DateTimeField):
				value = getattr(object, field.name)
				if isinstance(value, str):
					value = datetime.fromisoformat(value)
				if is_naive(value):
					value = make_aware(value, timezone=default_timezone)
				setattr(object, field.name, value)
		return object

	def save_objects(self, data_locations, metadatas, continue_on_fail=False):
		"""Save the metadata and their corresponding data location, matching them on the file_url"""
		with transaction.atomic():
			DataLocation.objects.bulk_create(data_locations.values(), ignore_conflicts=continue_on_fail)
			data_locations = dict(
				DataLocation.objects.filter(dataset=self.dataset, file_url__in=data_locations.keys()).values_list('file_url', 'id')
			)
			good_metadatas = []
			for file_url, metadata in metadatas.items():
				try:
					metadata.data_location_id = data_locations[file_url]
				except KeyError:
					if continue_on_fail:
						self.log.warning('Could not find DataLocation for URL %s, ignoring metadata with oid %s', file_url, metadata.oid)
					else:
						raise Exception('Could not find DataLocation for URL %s for metadata with oid %s' % (file_url, metadata.oid))
				else:
					good_metadatas.append(metadata)
			return self.dataset.metadata_model.objects.bulk_create(good_metadatas, ignore_conflicts=continue_on_fail)
