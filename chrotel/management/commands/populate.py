from django.core.management.base import BaseCommand, CommandError

from sunpy.net import vso
import pyfits
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

from chrotel.models import *

base_url = 'http://sdac.virtualsolar.org/cgi-bin/get/{provider}/{fileid}'

class Command(BaseCommand):
	help = 'Populate the Metada and DataLocation from vso'
	
	def add_arguments(self, parser):
		 parser.add_argument('start_date', type = lambda s: parse_date(s), help='The start date.')
		 parser.add_argument('end_date', nargs = '?', type = lambda s: parse_date(s), default = None, help='The end date.')
	
	def handle(self, **options):
		#import pdb; pdb.set_trace()
		
		end_date = options['end_date'] or datetime.utcnow()
		start_date = options['start_date']
		
		time_increment = timedelta(days = 1)
		instrument='ChroTel'
		client = vso.VSOClient()
		
		while start_date <= end_date:
			qr = client.query_legacy(start_date, min(start_date + time_increment, end_date), instrument=instrument)
			if qr.num_records() > 0:
				for record in qr:
					try:
						hdus = pyfits.open(record.fileid)
					except Exception, why:
						self.stdout.write(self.style.ERROR('Error opening file "%s": %s' % (record.fileid, why))) 
					try:
						meta_data = Metada.objects.create(id = record.time.start, fits_header = hdus[0].header.tostring())
						data_location = DataLocation.objects.create(meta_data = meta_data, url = base_url.format(provider=record.provider, fileid=record.fileid), file_size = record.size, thumbnail = record.extra.thumbnail.hires)
					except Exception, why:
						self.stdout.write(self.style.ERROR('Error creating record for "%s": %s' % (record.fileid, why)))
						print "", record.fileid, why
					else:
						self.stdout.write(self.style.SUCCESS('Created record for "%s"' % record.fileid)) 
			start_date += time_increment
