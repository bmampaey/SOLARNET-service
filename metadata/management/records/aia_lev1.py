from datetime import timedelta

from metadata.management import records
from metadata.models import AiaLev1

class RecordFromFitsFile(records.RecordFromFitsFile):
	'''Record created from a Fits file on disk'''
	
	metadata_model = AiaLev1
	exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax']
	HDU = 1
	
	#: The base directory in which are the files
	base_file_directory = '/data/SDO/'
	
	#: The base file URL 
	base_file_url = 'http://sdo.oma.be/data/'
	
	def get_relative_file_path(self):
		return self.file_path[39:]
	
	def get_thumbnail_url(self):
		return 'http://sdo.oma.be/PMD/preview_data/aia_lev1/{recnum}'.format(recnum = self.field_values['recnum'])
	
	def get_oid(self):
		return self.field_values['date_obs'].strftime('%Y%m%d%H%M%S') + '_%04d' % self.field_values['wavelnth']
	
	def get_field_values(self):
		
		field_values = super(RecordFromFitsFile, self).get_field_values()
		
		field_values['date_beg'] = field_values['date_obs']
		field_values['date_end'] = field_values['date_beg'] + timedelta(seconds=field_values['exptime'])
		# TODO check if there is a better value
		field_values['wavemin'] = field_values['wavemax'] = field_values['wavelnth'] / 10.0
		return field_values