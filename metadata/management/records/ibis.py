from datetime import timedelta
import pyfits
from metadata.management import records
from metadata.models import Ibis
from django.db import transaction

from dataset.models import DataLocation

class RecordFromFitsFile(records.RecordFromFitsFile):
	'''Record created from a Fits file on disk'''
	
	metadata_model = Ibis
	exclude_fields = ['date_beg', 'wavemin', 'wavemax']
	HDU = 1
	
	#: The base directory in which are the files
	base_file_directory = '/data/ibis/'
	
	#: The base file URL 
	base_file_url = 'http://solarnet.oma.be/data/ibis/'
	
	def get_extensions(self):
		return pyfits.open(self.file_path)
	
	def get_fits_header(self):
		'''Ibis fits header is a combination of the first HDU and the parsed HDU'''
		fits_header = self.extensions[0].header
		fits_header.update(self.extensions[self.hdu].header)
		return fits_header
	
	def get_relative_file_path(self):
		#import pdb; pdb.set_trace()
		return self.file_path[11:]
	
	def get_thumbnail_url(self):
		return None
	
	def get_oid(self):
		return self.field_values['channel'].lower() + '_' + self.field_values['date_obs'].strftime('%Y%m%d%H%M%S%f')
	
	def get_field_values(self):
		
		field_values = super(RecordFromFitsFile, self).get_field_values()
		
		field_values['date_beg'] = field_values['date_obs']
		# TODO check if there is a better value
		field_values['wavemin'] = field_values['wavemax'] = field_values['wavelnth'] / 10.0
		return field_values
	
	def save(self, tags = None, update = False):
		'''Save the record (DataLocation + MetaData) into the database'''
		
		for hdu in range(0, len(self.extensions)):
			self.hdu = hdu + 1
			print "Parsing HDU", hdu
			
			# If not update, skip file if metadata already exists
			if  update or not self.metadata_model.objects.filter(oid = self.oid).exists():
				# Create the corresponding DataLocation and Metadata
				# It needs to be an atomic transaction so that if the metadata creation fails, the data location is not saved
				with transaction.atomic():
					# Get or create data location (file_url is unique)
					data_location, created = DataLocation.objects.get_or_create(file_url = self.file_url, defaults = dict(file_size = self.file_size, file_path = self.relative_file_path, thumbnail_url = self.thumbnail_url))
					
					# Update or create metadata
					metadata, created = self.metadata_model.objects.update_or_create(oid = self.oid, defaults = dict(data_location = data_location, fits_header = self.fits_header.tostring(), **self.field_values))
					
					# Add the tags
					metadata.tags = tags
			
			# cleanup
			delattr(self, 'oid')
			delattr(self, 'field_values')
			delattr(self, 'fits_header')
			
		return data_location, metadata