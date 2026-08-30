import json

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.models import Count, Window

from dataset.models import Dataset
from project.utils import Logger

IGNORE_FIELDS = ['id', 'oid', 'date_beg', 'date_end', 'wavemin', 'wavemax', 'fits_header']
MAX_COUNTED_VALUES = 10
MAX_DISTINCT_VALUES = 3


class Command(BaseCommand):
	help = "Print the distinct values of the fields of a dataset's metadata model to find the ones with a unique value, and let the user set the constant value of the corresponding keywords"

	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The name of the dataset')
		parser.add_argument(
			'--ignore-field',
			'-i',
			default=IGNORE_FIELDS,
			action='append',
			metavar='NAME',
			help=f'Ignore field (default {", ".join(IGNORE_FIELDS)})',
		)
		parser.add_argument(
			'--analyze',
			'-a',
			action='store_true',
			help='Run ANALYZE on the metadata database table before fetching pg_stats info',
		)
		parser.add_argument(
			'--max-counted-values',
			'-c',
			type=int,
			default=MAX_COUNTED_VALUES,
			metavar='MAX',
			help=f'Maximum number of distinct values to fetch from DB when counting (default {MAX_COUNTED_VALUES})',
		)
		parser.add_argument(
			'--max-distinct-values',
			'-d',
			default=MAX_DISTINCT_VALUES,
			type=int,
			metavar='MAX',
			help='Maximum number of distinct values for a field to be considered constant (default {MAX_DISTINCT_VALUES})',
		)
		parser.add_argument(
			'--print-only',
			'-p',
			action='store_true',
			help='Do not set the keywords, only print the values',
		)
		parser.add_argument(
			'--backup-file',
			'-b',
			metavar='JSONL',
			help='Name of a JSONL file that contains a backup of the previously computed values',
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

		field_infos = self.restore_backup_file(options['backup_file'])

		# PostgreSQL keeps statistics about each column, and the most frequent values in table pg_stats
		# So to avoid counting the distinct values, which can be very long,
		# we use the pg_stats to discard fields for wich the DB knows the distinct count will be bigger than requested
		pgstats = self.get_table_pg_stats(metadata_model._meta.db_table, analyze=options['analyze'])

		for field in metadata_model._meta.get_fields():
			if field.is_relation:
				self.log.debug('Skip relational field %s', field.name)
				continue

			if field.name in options['ignore_field']:
				self.log.debug('Skip unwanted field %s', field.name)
				continue

			if field.name in field_infos:
				self.log.debug('Field was already counted %s', field.name)
				continue

			counted = False

			# Get the pg_stats of the database column corresponding to the field
			db_column = field.db_column or field.name

			try:
				distinct_count, distinct_values = pgstats[db_column]
				self.log.info(
					'pg_stats for column %s : %s distinct values, %s',
					db_column,
					distinct_count,
					', '.join(f'{v} : {c}' for v, c in distinct_values.items()),
				)
			except KeyError:
				self.log.info('No pg_stats for column %s', db_column)
				distinct_count, distinct_values = None, {}

			# If pg_stats reports a small number of distinct values
			# force counting so that we do not set a constant value based on erroneous statistics
			if not distinct_values or (distinct_count is None) or (distinct_count <= options['max_distinct_values']):
				distinct_count, distinct_values = self.get_field_most_frequent_values(
					metadata_model, field.name, options['max_counted_values']
				)
				counted = True

				self.log.info(
					'counted for column %s : %s distinct values, %s',
					db_column,
					distinct_count,
					', '.join(f'{v} : {c}' for v, c in distinct_values.items()),
				)

			field_infos[field.name] = {
				'field_name': field.name,
				'distinct_count': distinct_count,
				'distinct_values': distinct_values,
				'counted': counted,
			}

		self.log.debug(
			'List of fields that can be ignored safely %s',
			' '.join(f'-i {f}' for f, i in field_infos.items() if i['distinct_count'] > 2),
		)

		self.save_backup_file(options['backup_file'], field_infos)

		if not options['print_only']:
			for field_name, info in field_infos.items():
				if (field_name not in options['ignore_field']) and (info['distinct_count'] <= options['max_distinct_values']):
					try:
						keyword = dataset.keywords.get(name=field_name)
					except ObjectDoesNotExist:
						self.log.error('Dataset %s does not have a keyword named %s, skipping', dataset, field_name)
					else:
						self.set_keyword_constant_value(keyword, info['distinct_values'])

	def get_table_pg_stats(self, table_name, analyze=False):

		self.log.debug('Fetching pg_stats for table %s', table_name)

		pg_stats_map = {}

		with connection.cursor() as cursor:
			if analyze:
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

				distinct_values = {}

				# most_common_freqs and most_common_vals are not always available in pg_stats
				if isinstance(row[2], list):
					for value, count in sorted(zip(row[2], row[3])):
						distinct_values[str(value)] = count

				pg_stats_map[row[0]] = (distinct_count, distinct_values)

		return pg_stats_map

	def get_field_most_frequent_values(self, metadata_model, field_name, max_count):
		self.log.debug('Counting distinct values for field %s', field_name)

		result = (
			metadata_model.objects
			.values(field_name)
			.annotate(value_count=Count(field_name))
			.annotate(distinct_count=Window(expression=Count('*')))
			.order_by('-distinct_count')[:max_count]
		)
		return result[0]['distinct_count'], {str(item[field_name]): item['value_count'] for item in result}

	def set_keyword_constant_value(self, keyword, distinct_values):
		"""Set the constant_value of the keyword by letting the user choose one of the most frequent values"""

		options = list(distinct_values.items())

		# Ask user to select between possible options
		if len(options) > 1:
			print(f'Keyword {keyword.name} has {len(options)} distinct values, select an option below')
		else:
			print(f'Keyword {keyword.name} has a single value, select an option below')
		print(f'[C] {keyword.constant_value}')
		for i, (value, count) in enumerate(options):
			print(f'[{i}] "{value}" {count} occurences')
		print('[U] Unset constant (None)')
		print('[M] Manual input')
		print('[D] Delete keyword')

		new_constant_value = keyword.constant_value

		while True:
			selection = input('Please enter one of the options between [] or enter to keep the current one: ') or 'C'
			if selection == 'C':
				break
			elif selection == 'U':
				new_constant_value = None
				break
			elif selection == 'M':
				value = input('Please enter the value:')
				break
			elif selection.isdecimal() and int(selection) < len(options):
				new_constant_value = options[int(selection)][0]
				break
			elif selection == 'D':
				if self.delete_keyword(keyword):
					return
			else:
				print('Invalid selection', selection)

		if keyword.constant_value != new_constant_value:
			self.log.info(
				'Changing keyword %s constant value from "%s" to "%s"', keyword, keyword.constant_value, new_constant_value
			)
			keyword.constant_value = new_constant_value
			try:
				keyword.save()
			except ValidationError:
				print(f'Invalid value "{new_constant_value}" for keyword type {keyword.type}')
				self.set_keyword_constant_value(keyword, distinct_values)
		else:
			self.log.info('Not changing keyword %s constant value "%s"', keyword, keyword.constant_value)

	def delete_keyword(self, keyword):
		"""Ask confirmation and delete a keyword in the Database"""
		while True:
			selection = input(f'Are you sure you want to delete the keyword {keyword.name} ? [Y/N] ')
			if selection == 'Y':
				keyword.delete()
				self.log.info('Deleted keyword %s', keyword.name)
				return True
			elif selection == 'N':
				self.log.info('Kept keyword %s', keyword.name)
				return False
			else:
				print('Invalid selection', selection)

	def restore_backup_file(self, backup_file):
		data = {}
		try:
			with open(backup_file, 'rt') as file:
				data = {item['field_name']: item for item in (json.loads(line) for line in file if line.strip())}
		except Exception as error:
			self.log.info('Could not read backup file %s: %s', backup_file, error)

		return data

	def save_backup_file(self, backup_file, data):
		if not backup_file:
			for item in data.values():
				print(json.dumps(item))
		else:
			with open(backup_file, 'wt') as file:
				file.writelines(json.dumps(item) + '\n' for item in data.values())
