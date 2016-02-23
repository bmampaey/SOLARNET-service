from dataset.management.populate import PopulateFilesystem

class Populate(PopulateFilesystem):
	dataset = 'eit'
	directory = '/data/soho-archive/eit/lz'
	file_url_template = 'http://sidc.be/eitlz/{year}/{month}/{filename}'
	thumbnail_url_template = None
	
	def __init__(self, log = logging):
		
		if self.dataset is None:
			raise ImproperlyConfigured('dataset has not been set')
		
		if self.directory is None:
			raise ImproperlyConfigured('directory has not been set')
		
		self.metadata_model = Dataset.objects.get(id=dataset).metadata_model
		self.log = log
	
	def get_oid(self, header):
		'''Return the oid for the record'''
		return parse_date(header['DATE_OBS']).strftime('%Y%m%d%H%M%s')
	
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
	
	def get_fits_header(file_path):
		'''Return the header and file size for the record'''
		hdus = pyfits.open(file_path)
		file_size = os.path.getsize(file_path)
		
		return hdus[self.hdu_number], file_size
	
	def get_field_values(fields, header):
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
	
	def list_files(start_date = None, end_date = None):
		from glob import glob
		from itertools import chain
		return (chain.from_iterable(glob(os.path.join(x[0], '*.fits')) for x in os.walk(self.directory)))
	
	def run(self, start_date, end_date, update = False):
		'''Populate database with data location and metadata from file'''
		# List of fields to populate
		fields = self.metadata_model._meta.get_fields()
		
		for file_path in list_files(start_date, end_date):
			
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

