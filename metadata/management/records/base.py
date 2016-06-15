import os
import requests
import StringIO
import pyfits
import zlib
from dateutil.parser import parse as parse_date

from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.models.fields import DateField

from dataset.models import DataLocation


class RecordFromFitsFile(object):
	'''Record created from a Fist file on disk'''
	#: The Matadata model for the dataset
	metadata_model = None
	
	#: Fields to exclude from record
	exclude_fields = []
	
	#: The HDU for this record (a number or a name)
	HDU = 0
	
	#: The base directory in which are the files
	base_file_directory = None
	
	#: The base file URL
	#: Assume that the content of base_file_directory is accessible under base_file_url
	#: Otherwise override get_file_url
	base_file_url = None
	
	def __init__(self, file_path, lax = False):
		
		if not getattr(self, 'metadata_model'):
			raise ImproperlyConfigured('Metadata model has not been set')
		
		#: The path to a fits file
		self.file_path = file_path
		
		#: If true, will not raise an exception if one of the metadata field is lacking or bad in the Fits header
		#: Unless the field is mandatory (null == False in the model)
		self.lax = lax
	
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
	
	def get_file_url(self):
		'''Return the URL of the data location'''
		if self.base_file_directory is None or self.base_file_url is None:
			raise ImproperlyConfigured('Please set base_file_directory  and base_file_url or override get_file_url')
		
		
		file_abspath = os.path.abspath(self.file_path)
		if not file_abspath.startswith(self.base_file_directory):
			raise ValueError('File path is not in directory %s: check base_file_directory' % self.base_file_directory)
		
		file_relpath = file_abspath[len(self.base_file_directory):]
		if file_relpath.startswith('/') and self.base_file_url.endswith('/'):
			file_relpath = file_relpath[:-1]
		return self.base_file_url + file_relpath

	
	def get_thumbnail_url(self):
		'''Return the URL of the thumbnail of the data location'''
		return None
	
	def get_fits_header(self):
		'''Return the Fits header of the file'''
		hdus = pyfits.open(self.file_path)
		fits_header = hdus[self.HDU].header
		hdus.close(output_verify='ignore')
		return fits_header
	
	def get_file_size(self):
		'''Return the size of the file'''
		return os.path.getsize(self.file_path)
	
	def get_field_values(self):
		'''Return a dict of values for each metadata field'''
		
		field_values = dict()
		
		for field in self.fields:
			try:
				# If the field is a date or a datetime, parse the keyword value into a datetime
				if isinstance(field, DateField):
					value = parse_date(self.fits_header[field.verbose_name])
				else:
					value = self.fits_header[field.verbose_name]
				# Convert the keyword value into the appropriate python type for the field
				field_values[field.name] = field.to_python(value)
			except Exception, why:
				if not self.lax:
					raise
		
		return field_values
	
	def save(self, tags = None, update = False):
		'''Save the record (DataLocation + MetaData) into the database'''
		
		# If not update, skip file if metadata already exists
		if not update and self.metadata_model.objects.filter(oid = self.oid).exists():
			return
		
		# Create the corresponding DataLocation and Metadata
		# It needs to be an atomic transaction so that if the metadata creation fails, the data location is not saved
		with transaction.atomic():
			# Get or create data location (file_url is unique)
			data_location, created = DataLocation.objects.get_or_create(file_url = self.file_url, defaults = dict(file_size = self.file_size, file_path = self.relative_file_path, thumbnail_url = self.thumbnail_url))
			
			# Update or create metadata
			metadata, created = self.metadata_model.objects.update_or_create(oid = self.oid, defaults = dict(data_location = data_location, fits_header = self.fits_header.tostring(), **self.field_values))
			
			# Add the tags
			metadata.tags = tags
		
		return data_location, metadata

class RecordFromVSO(RecordFromFitsFile):
	'''Record created from a VSO record'''
	#: The Matadata model for the dataset
	metadata_model = None
	#: Fields to exclude from record
	exclude_fields = []
	#: Name of the instrument in the VSO (case sensitive)
	instrument = None
	#: The minimum size of the fits header to read
	min_header_size = 2880
	#: The offset of the header in the file
	header_offset = 0
	#: If True, the file is assumed to be zipped
	#: If False, the file is assumed to be not zipped
	#: If None, try to guess from the file extension
	zipped = None
	
	def __init__(self, vso_record, lax = False):
		
		if not getattr(self, 'metadata_model'):
			raise ImproperlyConfigured('Metadata model has not been set')
		
		if not getattr(self, 'instrument'):
			raise ImproperlyConfigured('instrument has not been set')
		
		#: A VSO record
		self.vso_record = vso_record
		
		#: If true, will not raise an exception if one of the metadata field is lacking or bad in the Fits header
		#: Unless the field is mandatory (null == False in the model)
		self.lax = lax
		
	def get_oid(self):
		'''Return the observation identifier'''
		return self.vso_record.time.start
	
	def get_file_url(self):
		'''Return the URL of the data location'''
		return 'http://sdac.virtualsolar.org/cgi-bin/get/{provider}/{fileid}'.format(provider=self.vso_record.provider, fileid=self.vso_record.fileid)
	
	def get_header_file_url(self):
		'''Return the URL of the file with the header'''
		return self.file_url
	
	
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
	
	def get_fits_header(self):
		'''Return the Fits header of the file'''
		
		# Check if file is zipped
		if self.zipped is None:
			zipped = self.header_file_url.lower().endswith('.gz') or self.header_file_url.lower().endswith('.zip')
		else:
			zipped = self.zipped
		
		# If fits file is zipped, the response content must be decompressed before writing it to the pseudo file
		if zipped:
			decompressor = zlib.decompressobj(zlib.MAX_WBITS | 16)
		
		# We download the file by chunck, by specifying the desired range, until we have the complete Fits header
		range_start = self.header_offset
		range_end = self.header_offset + self.min_header_size
		
		# We store the response in a pseudo file for pyfits
		fits_file = StringIO.StringIO()
		
		while True:
			# We set the desired range in the HTTP header, note that both bounds are inclusive 
			response = requests.get(self.header_file_url, headers = {'Range': 'Bytes=%s-%s' % (range_start, range_end - 1)})
			
			if zipped:
				fits_file.write(decompressor.decompress(response.content))
			else:
				fits_file.write(response.content)
			
			# It is necessary to rewind the file for pyfits
			fits_file.seek(0)
			
			# Try to read a full header from the pseudo file, if header is partial, an IOError will be raised
			try:
				fits_header = pyfits.Header.fromfile(fits_file)
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
		# The file size is set by get_fits_header
		self.header = self.get_fits_header()
		return self.file_size