from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.models import Count

from dataset.models import Dataset
from project.utils import Logger


class Command(BaseCommand):
	help = 'Inspect the fields of a metadata model to find the ones that have a constant value'

	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The name of the dataset')
		parser.add_argument(
			'--force-count',
			'-f',
			nargs='?',
			const=True,
			default=3,
			type=int,
			help='Count the values even if the database statistics suggest the field is not constant (optionnaly specify a max count)',
		)
		parser.add_argument(
			'--max-distinct',
			'-c',
			type=int,
			default=2,
			help='Maximum number of distinct values for a field to be considered constant',
		)
		parser.add_argument(
			'--field-name',
			'-n',
			action='append',
			help='Limit the inspection to the provided field names, if not specified all fields will be used',
		)
		parser.add_argument(
			'--skip-analyze',
			'-s',
			action='store_true',
			help='Do not run ANALYZE on the metadata database table before fetching pg_stats info',
		)

	def handle(self, **options):
		# Create a logger
		self.log = Logger(self, options.get('verbosity', 2))

		# Get the dataset
		try:
			dataset = Dataset.objects.get(name=options['dataset'])
		except Dataset.DoesNotExist:
			raise CommandError('Dataset %s not found' % options['dataset'])

		metadata_model = dataset.metadata_model

		table_pg_stats = self.get_table_pg_stats(metadata_model._meta.db_table, skip_analyze=options['skip_analyze'])

		constant_fields = {}

		for field in metadata_model._meta.get_fields():
			if options['field_name'] and field.name not in options['field_name']:
				self.log.debug('Skip unwanted field %s', field.name)
				continue

			db_column = field.db_column or field.name

			try:
				column_pg_stats = table_pg_stats[db_column]
				self.log.info('pg_stats for column %s : %s', db_column, column_pg_stats)
			except KeyError:
				self.log.info('No pg_stats for column %s', db_column)
				column_pg_stats = None

			if (
				(column_pg_stats is None)
				or (options['force_count'] is True)
				or (column_pg_stats['distinct_count'] < options['force_count'])
			):
				self.log.debug('Counting actual distinct values for field %s', field.name)

				field_most_frequent_values = self.get_field_most_frequent_values(
					metadata_model, field.name, options['max_distinct'] + 1
				)
				self.log.info('Most frequent values for field %s : %s', field.name, field_most_frequent_values)

				if len(field_most_frequent_values) <= options['max_distinct']:
					constant_fields[field.name] = field_most_frequent_values

		if constant_fields:
			for field_name, values in constant_fields.items():
				print(f'{field_name}: {list(values.keys())}')
		else:
			self.log.info('No constant fields found')

	def get_table_pg_stats(self, table_name, skip_analyze=False):

		pg_stats_map = {}

		with connection.cursor() as cursor:
			if not skip_analyze:
				cursor.execute(f'ANALYZE {table_name};')

			cursor.execute(
				'SELECT reltuples AS estimated_row_count FROM pg_class WHERE relname = %s;',
				[table_name],
			)
			row_count = cursor.fetchone()[0]

			cursor.execute(
				'SELECT attname, n_distinct, most_common_freqs, most_common_vals::text::text[] FROM pg_stats WHERE tablename = %s;',
				[table_name],
			)

			for row in cursor.fetchall():
				self.log.debug('%s', row)
				# when n_distinct is negative, the value is relative to the number of rows
				if row[1] < 0:
					distinct_count = -row[1] * row_count
				else:
					distinct_count = row[1]

				# most_common_freqs and most_common_vals are not always available in pg_stats
				if isinstance(row[2], list):
					most_frequent_values = list(sorted(zip(row[2], row[3])))

				else:
					most_frequent_values = None

				pg_stats_map[row[0]] = {'distinct_count': distinct_count, 'most_frequent_values': most_frequent_values}

		return pg_stats_map

	def get_field_most_frequent_values(self, metadata_model, field_name, max_count):
		most_frequent_values = (
			metadata_model.objects.values(field_name).annotate(count=Count(field_name)).order_by('-count')[:max_count]
		)
		return {item[field_name]: item['count'] for item in most_frequent_values}
