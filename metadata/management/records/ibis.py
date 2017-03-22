from datetime import timedelta
from metadata.management.records import FitsRecordFromDisk
from metadata.models import Ibis


class Record(FitsRecordFromDisk):
	metadata_model = Ibis
	exclude_fields = ['date_beg', 'wavemin', 'wavemax']
	hdu = 1
	
	#: The base directory in which are the files
	base_file_directory = '/data/ibis/'
	
	#: The base file URL 
	base_file_url = 'http://solarnet.oma.be/data/ibis/'
	
	def get_fits_header(self):
		'''Ibis fits header is a combination of the first HDU and the parsed HDU'''
		fits_header = self.extensions[0].header
		fits_header.update(self.extensions[self.hdu].header)
		return fits_header
	
	def get_relative_file_path(self):
		#import pdb; pdb.set_trace()
		return self.file_path[11:]
	
	def get_oid(self):
		return self.field_values['channel'].lower() + '_' + self.field_values['date_obs'].strftime('%Y%m%d%H%M%S%f')
	
	def get_field_values(self):
		
		field_values = super(Record, self).get_field_values()
		
		field_values['date_beg'] = field_values['date_obs']
		# TODO check if there is a better value
		field_values['wavemin'] = field_values['wavemax'] = field_values['wavelnth'] / 10.0
		return field_values
	
	def create(self, tags = None, update = False):
		# Ibis has more than one image per file
		# So we save them all as separate metadata
		for hdu in range(1, len(self.extensions)):
			self.hdu = hdu
			self.log.info('Processing HDU %s', self.hdu)
			
			super(Record, self).create(tags=tags, update=update)
			
			# Cleanup all the fields that have been set by create
			delattr(self, 'oid')
			delattr(self, 'field_values')
			delattr(self, 'fits_header')
