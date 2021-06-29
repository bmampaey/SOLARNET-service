import os
import requests
import io
import zlib
import logging
from astropy.io import fits

from dateutil.parser import parse as parse_date

from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.models.fields import DateField

from dataset.models import DataLocation

class FitsRecord(object):
	'''Record that allow to create metadata from fits'''
	
	#: The Matadata model for the dataset
	metadata_model = None
	
	#: Fields to exclude from record
	exclude_fields = []
	
	def __init__(self, log=logging, **kwargs):
		
		if not getattr(self, 'metadata_model'):
			raise ImproperlyConfigured('metadata_model has not been set')
		
		self.log = log
		
		for key, value in kwargs.items():
			setattr(self, key, value)
	
	def __getattr__(self, attr):
		'''Lazy load the attributes'''
		
		if not hasattr(self, 'get_' + attr):
			raise AttributeError('object has no attribute %s and no get method for this attribute' % attr)
		else:
			attr_value = getattr(self, 'get_' + attr)()
			setattr(self, attr, attr_value)
		return attr_value
	
	def get_fields(self):
		'''Return the metadata fields'''
		exclude_fields = ['id', 'data_location', 'tags', 'oid', 'fits_header'] + self.exclude_fields
		return [field for field in self.metadata_model._meta.get_fields() if field.name not in exclude_fields]
	
	def get_oid(self):
		'''Return the observation identifier'''
		return self.field_values['date_beg'].strftime('%Y%m%d%H%M%S')
	
	def get_file_size(self):
		'''Return the size of the file'''
		raise NotImplementedError('get_file_size has not been implemented')
	
	def get_relative_file_path(self):
		'''Return the relative file path for the data location'''
		raise NotImplementedError('get_relative_file_path has not been implemented')
	
	def get_file_url(self):
		'''Return the URL of the data location'''
		raise NotImplementedError('get_file_url has not been implemented')
	
	def get_thumbnail_url(self):
		'''Return the URL of the thumbnail of the data location'''
		return None
	
	def get_fits_header(self):
		'''Return the fits header of the file'''
		raise NotImplementedError('get_fits_header has not been implemented')
	
	def get_field_values(self):
		'''Return a dict of values for each metadata field'''
		
		field_values = dict()
		
		for field in self.fields:
			try:
				field_value = self.fits_header[field.verbose_name]
			except KeyError:
				self.log.error('Missing keyword %s in fits header', field.verbose_name)
				continue
			
			# If the field is a date or a datetime, parse the keyword value into a datetime
			if isinstance(field, DateField):
				try:
					field_value = parse_date(field_value)
				except ValueError:
					self.log.error('Could not parse value %s to datetime', field_value)
			
			# Convert the keyword value into the appropriate python type for the field
			try:
				field_values[field.name] = field.to_python(field_value)
			except Exception as why:
				self.log.error('Could not convert value %s to type %s: %s', field_value, field.__class__.__name__, why)
		
		return field_values
	
	def create(self, tags = None, update = False):
		'''Create the Metadata object and the DataLocation object into the database'''
		
		# If not update, skip file if metadata already exists
		if not update and self.metadata_model.objects.filter(oid = self.oid).exists():
			self.log.info('Metadata with oid %s exists already and update is false, skipping', self.oid)
			return None
		else:
			# Create the corresponding DataLocation and Metadata
			# It needs to be an atomic transaction so that if the metadata creation fails, the data location is not saved
			with transaction.atomic():
				# Get or create data location (file_url is unique)
				data_location, created = DataLocation.objects.get_or_create(file_url = self.file_url, defaults = dict(file_size = self.file_size, file_path = self.relative_file_path, thumbnail_url = self.thumbnail_url))
				
				if created:
					self.log.info('Created DataLocation for file url %s', self.file_url)
				
				# Update or create metadata
				metadata, created = self.metadata_model.objects.update_or_create(oid = self.oid, defaults = dict(data_location = data_location, fits_header = self.fits_header.tostring(), **self.field_values))
				
				if created:
					self.log.info('Created Metadata with oid %s', self.oid)
				else:
					self.log.info('Updated Metadata with oid %s', self.oid)
				
				# Add the tags
				if tags:
					metadata.tags.add(*tags)
			
			return data_location, metadata
	
	@classmethod
	def update(cls, metadata):
		'''Update an existing metadata from it's fits header'''
		
		record = cls(None, fits_header = fits.Header.fromstring(metadata.fits_header), oid = metadata.oid)
		for field, value in list(record.field_values.items()):
			setattr(metadata, field, value)
		metadata.save()


class FitsRecordFromDisk(FitsRecord):
	'''FitsRecord for a fits file on disk'''
	
	#: The default HDU for this record (a number or a name)
	hdu = 0
	
	#: The base directory in which are the files
	base_file_directory = None
	
	#: The base file URL
	#: Assume that the content of base_file_directory is accessible under base_file_url
	#: Otherwise override get_file_url
	base_file_url = None
	
	def __init__(self, file_path, hdu = None, **kwargs):
		
		super(FitsRecordFromDisk, self).__init__(**kwargs)
		
		self.file_path = file_path
		
		if hdu is not None:
			self.hdu = hdu
	
	def get_file_size(self):
		return os.path.getsize(self.file_path)
	
	def get_file_url(self):
		if self.base_file_directory is None or self.base_file_url is None:
			raise ImproperlyConfigured('Please set base_file_directory  and base_file_url or override get_file_url')
		
		file_abspath = os.path.abspath(self.file_path)
		if not file_abspath.startswith(self.base_file_directory):
			raise ValueError('File path is not in directory %s: check base_file_directory' % self.base_file_directory)
		
		file_relpath = file_abspath[len(self.base_file_directory):]
		if file_relpath.startswith('/') and self.base_file_url.endswith('/'):
			file_relpath = file_relpath[:-1]
		return self.base_file_url + file_relpath
	
	def get_extensions(self):
		'''Return the fits file extensions'''
		return fits.open(self.file_path)
	
	def get_fits_header(self):
		'''Return the fits header of the file'''
		return self.extensions[self.hdu].header

class FitsRecordFromHTTP(FitsRecord):
	'''FitsRecord for a fits file via HTTP'''
	
	#: The minimum size of the fits header to read
	min_header_size = 2880
	
	#: The offset of the header in the file
	header_offset = 0
	
	#: If True, the file is assumed to be zipped
	#: If False, the file is assumed to be not zipped
	#: If None, try to guess from the file extension
	zipped = None
	
	#: Authentication for the webserver
	auth = None
	
	def __init__(self, file_url, **kwargs):
		
		super(FitsRecordFromHTTP, self).__init__(**kwargs)
		
		self.file_url = file_url
	
	def get_fits_header(self):
		
		# Check if file is zipped
		if self.zipped is None:
			zipped = self.file_url.lower().endswith('.gz') or self.file_url.lower().endswith('.zip')
		else:
			zipped = self.zipped
		
		# If fits file is zipped, the response content must be decompressed before writing it to the pseudo file
		if zipped:
			decompressor = zlib.decompressobj(zlib.MAX_WBITS | 16)
		
		# We download the file by chunk, by specifying the desired range, until we have the complete Fits header
		range_start = self.header_offset
		range_end = self.header_offset + self.min_header_size
		
		# We store the response in a pseudo file for the fits library
		fits_file = io.StringIO()
		
		while True:
			self.log.debug('Reading file %s from %s to %s', self.file_url, range_start, range_end - 1)
			# We set the desired range in the HTTP header, note that both bounds are inclusive
			response = requests.get(self.file_url, headers = {'Range': 'Bytes=%s-%s' % (range_start, range_end - 1)}, auth=self.auth)
			
			if zipped:
				fits_file.write(decompressor.decompress(response.content))
			else:
				fits_file.write(response.content)
			
			# It is necessary to rewind the file to pass it to the fits library
			fits_file.seek(0)
			
			# Try to read a full header from the pseudo file, if header is partial, an IOError will be raised
			try:
				fits_header = fits.Header.fromfile(fits_file)
			except IOError:
				# Header is partial, we need to read more from the file
				# Per fits standard, fits file header size is always a multiple of 2880
				range_start = range_end
				range_end = range_start + 2880
			else:
				# Header is complete
				# Extract the real file size from the response header
				if 'content-range' in response.headers:
					self.file_size = int(response.headers['content-range'].split('/')[1])
				else:
					self.file_size = int(response.headers['content-length'])
				break
		
		return fits_header
	
	def get_file_size(self):
		'''Return the size of the file'''
		response = requests.head(self.file_url, auth=self.auth)
		return response.headers['content-length']

class FitsRecordFromVSO(FitsRecordFromHTTP):
	'''FitsRecord for a VSO record'''
	
	#: Name of the instrument in the VSO (case sensitive)
	instrument = None
	
	def __init__(self, vso_record, **kwargs):
		
		super(FitsRecordFromVSO, self).__init__(**kwargs)
		
		if not getattr(self, 'instrument'):
			raise ImproperlyConfigured('instrument has not been set')
		
		self.vso_record = vso_record
	
	def get_oid(self):
		return self.vso_record.time.start
	
	def get_file_url(self):
		return 'http://sdac.virtualsolar.org/cgi-bin/get/{provider}/{fileid}'.format(provider=self.vso_record.provider, fileid=self.vso_record.fileid)
	
	def get_thumbnail_url(self):
		'''Return the URL of the thumbnail of the data location'''
		
		# Try to return the URL of highest resolution thumbnail
		try:
			return self.vso_record.extra.thumbnail.highres
		except Exception:
			pass
		
		try:
			return self.vso_record.extra.thumbnail.lowres
		except Exception:
			pass
		
		return None
	
	def get_corrected_file_url(self):
		'''Return the corrected file URL to read the header'''
		return self.file_url
	
	def get_fits_header(self):
		# In some cases, the file_url for the VSO record is incorrect
		# thus we need to correct it before getting the header
		file_url_backup, self.file_url = self.file_url, self.corrected_file_url
		header = super(FitsRecordFromVSO, self).get_fits_header()
		self.file_url = file_url_backup
		return header
