from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from urlparse import urlparse

from django.core.management.base import BaseCommand
from django.db import transaction

from sunpy.net import vso

from _tools import get_fits_header

from common.models import DataLocation
from chrotel.models import Metadata

base_url = 'http://sdac.virtualsolar.org/cgi-bin/get/{provider}/{fileid}'


class Command(BaseCommand):
	help = 'Populate the Metada and DataLocation from VSO'
	
	def add_arguments(self, parser):
		parser.add_argument('start_date', type = lambda s: parse_date(s), help='The start date.')
		parser.add_argument('end_date', nargs = '?', type = lambda s: parse_date(s), default = None, help='The end date.')
		parser.add_argument('--time_increment', type = int, default = 1, help='The number of hours to request at a time.')
		parser.add_argument('--update', default = False, action='store_true', help='Update metadata even if already present in DB')
		
	def handle(self, **options):
		# Parse the options
		end_date = options['end_date'] or datetime.utcnow()
		start_date = options['start_date']
		time_increment = timedelta(hours = options['time_increment'])
		update = options['update']
		
		# Instrument specific constants
		instrument='ChroTel'
		header_size = 5760
		
		client = vso.VSOClient()
		while start_date <= end_date:
			for record in client.query_legacy(start_date, min(start_date + time_increment, end_date), instrument=instrument):
				# Skip element if metadata already exists
				if not update and Metadata.objects.filter(oid = record.time.start).exists():
					self.stdout.write(self.style.WARNING('Not updating data_location and metadata for file "%s"' % record.fileid)) 
					continue
				# For ChroTel the url is ftp, but it can be changed to http for partial download
				url = urlparse(record.fileid)._replace(scheme='http').geturl()
				
				# Get the header
				try:
					file_size, header = get_fits_header(url, header_size, zipped = True)
				except Exception, why:
					self.stdout.write(self.style.ERROR('Error reading file "%s": %s' % (record.fileid, why)))
				
				# Create the corresponding DataLocation and Metadata
				try:
					# It needs to be an atomic transaction so that if the metadata creation fails, the data location is not saved
					with transaction.atomic():
						# Create data location but with access through VSO
						data_location = DataLocation.objects.create(url = base_url.format(provider=record.provider, fileid=record.fileid), size = file_size, thumbnail = record.extra.thumbnail.lowres)
						# Create metadata
						metadata = Metadata.objects.create(oid = record.time.start, data_location = data_location, fits_header = header.tostring())
				except Exception, why:
					self.stdout.write(self.style.ERROR('Error creating record for "%s": %s' % (record.fileid, why)))
				else:
					self.stdout.write(self.style.SUCCESS('Created record for "%s"' % record.fileid))
			
			start_date += time_increment
