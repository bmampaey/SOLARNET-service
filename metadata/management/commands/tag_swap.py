from datetime import datetime
import pytz
import sqlite3

from django.core.management.base import BaseCommand, CommandError
from metadata.models import Tag, SwapLev1

class Command(BaseCommand):
	help = 'Add tags to Swap Levvel 1 metadata using swap event databases'
	
	def add_arguments(self, parser):
		parser.add_argument('tag', help='The name of the tag.')
		parser.add_argument('db_file', help='The path to the Swap event DB (sqlite3 file).')
		parser.add_argument('event_type_id', help='The id number of the event type.')
		
	def handle(self, **options):
		
		log = Logger(self)
		
		if not os.path.exists(options['db_file']):
			raise CommandError('DB file %s not found' % options['db_file'])
		
		tag, created = Tag.objects.get_or_create(name=options['tag'])
		if created:
			log.info('Created new tag %s', tag)
		
		db_connection = sqlite3.connect(options['db_file'], detect_types=sqlite3.PARSE_DECLTYPES)
		db_connection.row_factory = sqlite3.Row
		
		cursor = db_connection.execute('select begin_time, end_time from event where eventType_id = ? order by begin_time;', (options['event_type_id'], ))
		for row in cursor:
			begin_time = datetime.utcfromtimestamp(row['begin_time']).replace(tzinfo=pytz.utc)
			end_time = datetime.utcfromtimestamp(row['end_time']).replace(tzinfo=pytz.utc)
			log.info('Tagging metadata from %s to %s with tag "%s"', begin_time, end_time, tag.name)
			for metadata in SwapLev1.objects.filter(date_obs__range=(begin_time, end_time)):
				metadata.tags.add(tag)