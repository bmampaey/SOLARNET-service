import logging
from datetime import timedelta
from urlparse import urlparse
from dateutil.parser import parse as parse_date
from django.db import transaction
from django.db.models.fields import DateField

from sunpy.net import vso

from dataset.management.tools import get_fits_header
from dataset.models import DataLocation
from chrotel.models import Metadata


class PopulateVSO:
	vso_base_url = 'http://sdac.virtualsolar.org/cgi-bin/get/{provider}/{fileid}'
	min_header_size = 2880
	zipped = False
	time_increment = timedelta(hours = 1)
	
	def __init__(self, log = logging):
		self.log = log
	
	def get_oid(self, record):
		return record.time.start
	
	def get_file_url(self, record):
		return urlparse(record.fileid)._replace(scheme='http').geturl()
	
	def get_thumbnail_url(self, record):
		
		thumbnail_url = None
		
		try:
			thumbnail_url = record.extra.thumbnail.highres
		except Exception:
			log.debug('No highres thumbnail for record %s', record.fileid)
		try:
			thumbnail_url = record.extra.thumbnail.lowres
		except Exception:
			log.debug('No thumbnail for record %s', record.fileid)
		return thumbnail_url
	
	def get_data_location(self, record):
		return vso_base_url.format(provider=record.provider, fileid=record.fileid)
	
	def run(self, start_date, end_date, update = False):
		# We use the sunpy VSO client to find the files
		client = vso.VSOClient()
		
		while start_date <= end_date:
			for record in client.query_legacy(start_date, min(start_date + self.time_increment, end_date), instrument=self.instrument):
				
				# Skip element if metadata already exists
				if not update and Metadata.objects.filter(oid = self.get_oid(record)).exists():
					log.warning('Not updating data_location and metadata for file "%s"', record.fileid) 
					continue
				
				# Get file and thumbnail url
				# For ChroTel the url is ftp, but it can be changed to http for partial download
				file_url = self.get_file_url(record)
				thumbnail_url = self.get_thumbnail_url(record)
				
				# Get the header
				try:
					file_size, header = get_fits_header(file_url, self.min_header_size, self.zipped)
				except Exception, why:
					log.error('Error reading file "%s": %s', record.fileid, why)
					continue
				
				# Create the corresponding DataLocation and Metadata
				try:
					# It needs to be an atomic transaction so that if the metadata creation fails, the data location is not saved
					with transaction.atomic():
						# Create data location but with access through VSO
						data_location = DataLocation.objects.create(file_url = self.get_data_location(record), file_size = file_size, thumbnail_url = thumbnail_url)
						# Create metadata
						metadata = Metadata.objects.create(oid = self.get_oid(record), data_location = data_location, fits_header = header.tostring())
				
				except Exception, why:
					log.error('Error creating record for "%s": %s', record.fileid, why)
				
				else:
					log.info('Created record for "%s"', record.fileid)
			
			start_date += time_increment

def populate(start_date, end_date, update, log):
	'''Populate the Metadata and DataLocation'''
	
	# Dataset specific constants
	instrument='ChroTel'
	header_size = 5760
	zipped = True
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
			# For ChroTel the url is ftp, but it can be changed to http for partial download
			url = urlparse(record.fileid)._replace(scheme='http').geturl()
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
					# Create data location but with access through VSO
					data_location = DataLocation.objects.create(file_url = vso_base_url.format(provider=record.provider, fileid=record.fileid), file_size = file_size, thumbnail_url = thumbnail_url)
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
		
	# See http://www.kis.uni-freiburg.de/en/observatories/chrotel/data/
	values['date_beg'] = values['date_obs']
	values['date_end'] = values['date_obs'] + timedelta(seconds = values['exptime'])
	full_width_at_half_maximum = {
		393.4 : 0.03,
		656.2 : 0.05,
		1083.0: 0.14
	}
	values['wavemin'] = values['wavelnth'] - full_width_at_half_maximum[values['wavelnth']]
	values['wavemax'] = values['wavelnth'] + full_width_at_half_maximum[values['wavelnth']]
	
	return values