from datetime import timedelta

from dataset.management import records
from ..models import Metadata

class RecordFromFitsFile(records.RecordFromFitsFile):
	'''Record created from a Fist file on disk'''
	
	metadata_model = Metadata
	exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax']
	HDU = 1
	
	#: The base directory in which are the files
	base_file_directory = '/data/SDO/'
	
	#: The base file URL 
	base_file_url = 'http://sdo.oma.be/data/'
	
	def get_thumbnail_url(self):
		return 'http://sdo.oma.be/PMD/preview_data/hmi_m_45s/{recnum}'.format(recnum = self.field_values['recnum'])
	
	def get_field_values(self):
		
		field_values = super(RecordFromFitsFile, self).get_field_values()
		
		field_values['date_beg'] = field_values['date_obs']
		field_values['date_end'] = field_values['date_beg'] + timedelta(seconds=field_values['exptime'])
		# Taken from VSO
		field_values['wavemin'] = 6173 / 10.0
		field_values['wavemax'] = 6174 / 10.0
		 = field_values['wavelnth'] / 10.0
		return field_values