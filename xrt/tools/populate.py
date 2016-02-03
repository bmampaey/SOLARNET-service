from datetime import timedelta
from django.db import transaction

from sunpy.net import vso

from common.tools import get_fits_header
from common.models import DataLocation
from xrt.models import Metadata


def populate(start_date, end_date, update, log):
	'''Populate the Metada and DataLocation'''
	
	# Dataset specific constants
	instrument='XRT'
	header_size = 20160
	zipped = False
	time_increment = timedelta(hours = 1)
	vso_base_url = 'http://sdac.virtualsolar.org/cgi-bin/get/{provider}/{fileid}'
	
	# This dataset is populated through the VSO
	client = vso.VSOClient()
	
	while start_date <= end_date:
		for record in client.query_legacy(start_date, min(start_date + time_increment, end_date), instrument=instrument):
			
			# Skip element if metadata already exists
			if not update and Metadata.objects.filter(oid = record.time.start).exists():
				log.warning('Not updating data_location and metadata for file "%s"', record.fileid) 
				continue
			
			# Get file and thumbnail url
			url = record.fileid
			try:
				thumbnail = record.extra.thumbnail.highres
			except Exception:
				try:
					thumbnail = record.extra.thumbnail.lowres
				except Exception:
					thumbnail = None
					log.warning("No thumbnail for file %s", record.fileid)
			
			# Get the header
			try:
				file_size, header = get_fits_header(url, header_size, zipped)
			except Exception, why:
				log.error('Error reading file "%s": %s', record.fileid, why)
				continue
			
			# Create the corresponding DataLocation and Metadata
			try:
				# It needs to be an atomic transaction so that if the metadata creation fails, the data location is not saved
				with transaction.atomic():
					# Create data location but with access through VSO
					data_location = DataLocation.objects.create(url = vso_base_url.format(provider=record.provider, fileid=record.fileid), size = file_size, thumbnail = thumbnail)
					# Create metadata
					metadata = Metadata.objects.create(oid = record.time.start, data_location = data_location, fits_header = header.tostring())
			
			except Exception, why:
				log.error('Error creating record for "%s": %s', record.fileid, why)
			
			else:
				log.info('Created record for "%s"', record.fileid)
		
		start_date += time_increment
