from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from sunpy.net import vso

from _tools import get_fits_header
from common.models import DataLocation
from xrt.models import Metadata

vso_base_url = 'http://sdac.virtualsolar.org/cgi-bin/get/{provider}/{fileid}'

class Command(BaseCommand):
	help = 'Populate the Metada and DataLocation from VSO'
	
	def add_arguments(self, parser):
		parser.add_argument('start_date', type = lambda s: parse_date(s), help='The start date.')
		parser.add_argument('end_date', nargs = '?', type = lambda s: parse_date(s), default = None, help='The end date.')
		parser.add_argument('--time_increment', type = int, default = 1, help='The number of hours to request at a time.')
		parser.add_argument('--header_size', type = int, default = 20160, help='The estimated size of the header (multiple of 2880).')
		
	def handle(self, **options):
		end_date = options['end_date'] or datetime.utcnow()
		start_date = options['start_date']
		header_size = options['header_size']
		time_increment = timedelta(hours = options['time_increment'])
		
		instrument='XRT'
		
		client = vso.VSOClient()
		
		while start_date <= end_date:
			qr = client.query_legacy(start_date, min(start_date + time_increment, end_date), instrument=instrument)
			if qr.num_records() > 0:
				for record in qr:
					try:
						file_size, header = get_fits_size_header(record.fileid, header_size)
					except Exception, why:
						self.stdout.write(self.style.ERROR('Error opening file "%s": %s' % (record.fileid, why))) 
					try:
						# It needs to be an atomic transaction so that if the metadata creation fails, the data location is not saved
						with transaction.atomic():
							# Create data location but with acces through VSO
							data_location = DataLocation.objects.create(url = base_url.format(provider=record.provider, fileid=record.fileid), size = file_size, thumbnail = record.extra.thumbnail.lowres)
							# Create metadata
							metadata = Metadata.objects.create(oid = record.time.start, data_location = data_location, fits_header = header.tostring())
					except Exception, why:
						self.stdout.write(self.style.ERROR('Error creating record for "%s": %s' % (record.fileid, why)))
					else:
						self.stdout.write(self.style.SUCCESS('Created record for "%s"' % record.fileid)) 
			start_date += time_increment
