import logging
from datetime import timedelta
from urlparse import urlparse
from dateutil.parser import parse as parse_date
from django.db import transaction
from django.db.models.fields import DateField



from dataset.management.tools import get_fits_header
from dataset.models import DataLocation
from xrt.models import Metadata


def populate(start_date, end_date, update, log):
	'''Populate the Metadata and DataLocation'''
	
	# Dataset specific constants
	instrument='XRT'
	header_size = 20160
	zipped = False
	time_increment = timedelta(hours = 1)
	
	
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
				thumbnail_url = record.extra.thumbnail.highres
			except Exception:
				try:
					thumbnail_url = record.extra.thumbnail.lowres
				except Exception:
					thumbnail_url = None
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
					# Create data location but with access through VSO (xrt data is stored at VSO)
					data_location = DataLocation.objects.create(file_url = url, file_size = file_size, thumbnail_url = thumbnail_url)
					# Create metadata
					metadata = Metadata.objects.create(oid = record.time.start, data_location = data_location, fits_header = header.tostring())
			
			except Exception, why:
				log.error('Error creating record for "%s": %s', record.fileid, why)
			
			else:
				log.info('Created record for "%s"', record.fileid)
		
		start_date += time_increment

def field_values(fields, header):
	values = dict()
	for field in fields:
		try:
			if field.verbose_name in header:
				if isinstance(field, DateField):
					value = parse_date(header[field.verbose_name])
				else:
					value = header[field.verbose_name]
				values[field.name] = field.to_python(value)
		except Exception, why:
			print field.name, why
	
	# See https://xrt.cfa.harvard.edu/resources/documents/XAG/XAG.pdf
	values['date_beg'] = values['date_obs']
	full_width_at_half_maximum = 17
	values['wavemin'] = 430.5 - full_width_at_half_maximum
	values['wavemax'] = 430.5 + full_width_at_half_maximum
	
	return values