from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.models import Count

from dataset.models import Dataset
from project.utils import Logger


class Command(BaseCommand):
	help = 'List the names of datasets'

	def add_arguments(self, parser):
		parser.add_argument('--list-keywords', '-k', action='store_true', help='For each dataset, list the name of keywords')

	def handle(self, **options):
		# Create a logger
		self.log = Logger(self, options.get('verbosity', 2))

		# Get the dataset
		try:
			datasets = Dataset.objects.all()
		except Exception:
			raise CommandError('Could not fetch list of datasets')

		for dataset in datasets:
			print(f'"{dataset.name}"')
			if options['list_keywords']:
				for keyword in dataset.keywords.all():
					print(f'\t"{keyword.name}"')
