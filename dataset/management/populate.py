import os
import requests
import StringIO
import pyfits
import zlib
import logging
from datetime import timedelta
from dateutil.parser import parse as parse_date
from glob import glob
from itertools import chain

from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.models.fields import DateField
from sunpy.net import vso

from dataset.models import Dataset, DataLocation


def get_fits_header_via_http(url, zipped = False, min_size = 2880, header_start = 0):
	'''Try to extract the header from a fits file by doing a partial download of the url'''
	
	start = header_start
	end = header_start + min_size
	
	# We store the response in a pseudo file for pyfits
	fits_file = StringIO.StringIO()
	
	# If fits file is zipped, the response content must be decompressed before writing it to the pseudo file
	if zipped:
		decompressor = zlib.decompressobj(zlib.MAX_WBITS | 16)
	
	while True:
		# We download the file by chunck, by specifying the desired range in the header, both bounds are inclusive 
		response = requests.get(url, headers = {'Range': 'Bytes=%s-%s' % (start, end - 1)})
		
		if zipped:
			fits_file.write(decompressor.decompress(response.content))
		else:
			fits_file.write(response.content)
		
		# It is necessary to rewind the file for pyfits
		fits_file.seek(0)
		
		# Try to read a full header from the pseudo file, if header is partial, an IOError will be raised
		try:
			header = pyfits.Header.fromfile(fits_file)
		except IOError:
			# Header is partial, we need to read more from the file
			# Per fits standard, fits file header size is always a multiple of 2880 
			start = end
			end = start + 2880
		else:
			# Header is complete
			# Extract the real file size from the response header
			if 'content-range' in response.headers:
				file_size = int(response.headers['content-range'].split('/')[1])
			else:
				file_size = int(response.headers['content-length'])
			break
	
	return header, file_size


class PopulatorForVSO:
	vso_base_url = 'http://sdac.virtualsolar.org/cgi-bin/get/{provider}/{fileid}'
	min_header_size = 2880
	header_start = 0
	zipped = False
	time_increment = timedelta(hours = 1)
	instrument = None
	dataset_id = None
	
	def __init__(self, log = logging):
		
		if self.dataset_id is None:
			raise ImproperlyConfigured('dataset_id has not been set')
		if self.instrument is None:
			raise ImproperlyConfigured('dataset_id has not been set')
		
		self.metadata_model = Dataset.objects.get(id=dataset_id).metadata_model
		self.log = log
	
	def get_oid(self, record):
		'''Return the oid for the record'''
		return record.time.start
	
	def get_file_url(self, record):
		'''Return the file url for the record'''
		return vso_base_url.format(provider=record.provider, fileid=record.fileid)
	
	def get_thumbnail_url(self, record):
		'''Return the best thumbnail url for the record'''
		thumbnail_url = None
		
		try:
			thumbnail_url = record.extra.thumbnail.highres
		except Exception:
			self.log.debug('No highres thumbnail for record %s', record.fileid)
		try:
			thumbnail_url = record.extra.thumbnail.lowres
		except Exception:
			self.log.debug('No thumbnail for record %s', record.fileid)
		return thumbnail_url
	
	def get_fits_header(self, record):
		'''Return the header and file size for the record'''
		url = self.get_file_url(record)
		return get_fits_header_via_http(url, self.zipped, self.min_header_size, self.header_start)
	
	def get_field_values(self, fields, header):
		'''Return a dict with the value for each field'''
		field_values = dict()
		
		for field in fields:
			if field.verbose_name in header:
				try:
					# If the field is a data or a datetime, parse the keyword value into a datetime
					if isinstance(field, DateField):
						value = parse_date(header[field.verbose_name])
					else:
						value = header[field.verbose_name]
					# Convert the keyword value into the appropriate python type for the field
					field_values[field.name] = field.to_python(value)
				except Exception, why:
					self.log.error('Error parsing value %s for field %s: %s', header[field.verbose_name], field.name, why)
			else:
				self.log.warning('Missing keyword %s in header', field.verbose_name)
		
		return field_values
	
	def run(self, start_date, end_date, update = False):
		'''Populate database with data location and metadata from vso'''
		# We use the sunpy VSO client to find the files
		client = vso.VSOClient()
		
		# List of fields to populate
		fields = self.metadata_model._meta.get_fields()
		
		while start_date <= end_date:
			for record in client.query_legacy(start_date, min(start_date + self.time_increment, end_date), instrument=self.instrument):
				
				# Skip element if metadata already exists
				if not update and Metadata.objects.filter(oid = self.get_oid(record)).exists():
					self.log.warning('Not updating data_location and metadata for file "%s"', record.fileid) 
					continue
				
				# Get the header
				try:
					header, file_size = self.get_fits_header(record)
				except Exception, why:
					self.log.error('Error reading file "%s": %s', record.fileid, why)
					continue
				
				# Get the field values
				try:
					field_values = self.get_field_values(fields, header)
				except Exception, why:
					self.log.error('Error parsing header into field values "%s": %s', record.fileid, why)
					field_values = {}
					continue
				
				# Create the corresponding DataLocation and Metadata
				try:
					# It needs to be an atomic transaction so that if the metadata creation fails, the data location is not saved
					with transaction.atomic():
						# Create data location but with access through VSO
						data_location = DataLocation.objects.create(file_url = self.get_file_url(record), file_size = file_size, thumbnail_url = self.get_thumbnail_url(record))
						
						# Create metadata
						metadata = self.metadata_model.objects.create(oid = self.get_oid(record), data_location = data_location, fits_header = header.tostring(), **field_values)
				
				except Exception, why:
					self.log.error('Error creating record for "%s": %s', record.fileid, why)
				
				else:
					self.log.info('Created record for "%s"', record.fileid)
			
			start_date += time_increment


class PopulatorForFiles:
	dataset_id = None
	directory = None
	file_url_template = None
	thumbnail_url_template = None
	
	def __init__(self, log = logging):
		
		if self.dataset_id is None:
			raise ImproperlyConfigured('dataset_id has not been set')
		
		if self.directory is None:
			raise ImproperlyConfigured('directory has not been set')
		
		self.metadata_model = Dataset.objects.get(id=dataset_id).metadata_model
		self.log = log
	
	def get_oid(self, header):
		'''Return the oid for the record'''
		raise ImproperlyConfigured('get_oid must be overriden')
	
	def get_file_url(self, header):
		'''Return the file url for the record'''
		if self.file_url_template is None:
			raise ImproperlyConfigured('file_url_template has not been set. Set file_url_template or override get_file_url')
		else:
			return file_url_template.format(**dict(header.iteritems()))
	
	def get_thumbnail_url(self, header):
		'''Return the thumbnail url for the record'''
		thumbnail_url = None
		if self.thumbnail_url_template is None:
			self.log.warning('No thumbnail_url_template was set')
			return None
		else:
			return thumbnail_url_template.format(**dict(header.iteritems()))
	
	def get_fits_header(self, file_path):
		'''Return the header and file size for the record'''
		hdus = pyfits.open(file_path)
		file_size = os.path.getsize(file_path)
		
		return hdus[self.hdu_number], file_size
	
	def get_field_values(self, fields, header):
		'''Return a dict with the value for each field'''
		field_values = dict()
		
		for field in fields:
			if field.verbose_name in header:
				try:
					# If the field is a data or a datetime, parse the keyword value into a datetime
					if isinstance(field, DateField):
						value = parse_date(header[field.verbose_name])
					else:
						value = header[field.verbose_name]
					# Convert the keyword value into the appropriate python type for the field
					field_values[field.name] = field.to_python(value)
				except Exception, why:
					self.log.error('Error parsing value %s for field %s: %s', header[field.verbose_name], field.name, why)
			else:
				self.log.warning('Missing keyword %s in header', field.verbose_name)
		
		return field_values
	
	def list_files(self, start_date = None, end_date = None):
		return (chain.from_iterable(glob(os.path.join(x[0], '*.fits')) for x in os.walk(self.directory)))
	
	def run(self, start_date, end_date, update = False):
		'''Populate database with data location and metadata from file'''
		# List of fields to populate
		fields = self.metadata_model._meta.get_fields()
		
		for file_path in self.list_files(start_date, end_date):
			
			# Get the header
			try:
				header, file_size = self.get_fits_header(file_path)
			except Exception, why:
				self.log.error('Error reading file "%s": %s', file_path, why)
				continue
			
			# Skip element if metadata already exists
			if not update and Metadata.objects.filter(oid = self.get_oid(header)).exists():
				self.log.warning('Not updating data_location and metadata for file "%s"', file_path) 
				continue
			
			# Get the field values
			try:
				field_values = self.get_field_values(fields, header)
			except Exception, why:
				self.log.error('Error parsing header into field values "%s": %s', file_path, why)
				continue
			
			# Create the corresponding DataLocation and Metadata
			try:
				# It needs to be an atomic transaction so that if the metadata creation fails, the data location is not saved
				with transaction.atomic():
					# Create data location but with access through VSO
					data_location = DataLocation.objects.create(file_url = self.get_file_url(header), file_size = file_size, thumbnail_url = self.get_thumbnail_url(header))
					
					# Create metadata
					metadata = self.metadata_model.objects.create(oid = self.get_oid(header), data_location = data_location, fits_header = header.tostring(), **field_values)
			
			except Exception, why:
				self.log.error('Error creating record for "%s": %s', file_path, why)
				
				else:
					self.log.info('Created record for "%s"', file_path)

