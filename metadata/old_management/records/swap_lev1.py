import os
from datetime import timedelta

from metadata.management.records import FitsRecordFromDisk
from metadata.models import SwapLev1

class Record(FitsRecordFromDisk):
	metadata_model = SwapLev1
	exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax']
	hdu = 0
	
	#: The base directory in which are the files
	base_file_directory = '/data/proba2/swap/bsd/'
	
	#: The base file URL 
	base_file_url = 'http://proba2.oma.be/swap/data/bsd/'
	
	def get_relative_file_path(self):
		return self.file_path[22:]
	
	def get_thumbnail_url(self):
		return 'http://proba2.oma.be/swap/data/qlviewer/' + self.field_values['date_obs'].strftime('%Y/%m/%d/') + os.path.splitext(self.field_values['file_tmr'])[0] + '.png'
	
	def get_field_values(self):
		
		field_values = super(Record, self).get_field_values()
		
		field_values['date_beg'] = field_values['date_obs']
		field_values['date_end'] = field_values['date_beg'] + timedelta(seconds=field_values['exptime'])
		# TODO check if there is a better value
		field_values['wavemin'] = field_values['wavemax'] = field_values['wavelnth'] / 10.0
		return field_values