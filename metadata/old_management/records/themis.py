from dateutil.parser import parse as parse_date
from metadata.management.records import FitsRecordFromDisk
from metadata.models import Themis

class Record(FitsRecordFromDisk):
	metadata_model = Themis
	exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax']
	
	#: The base directory in which are the files
	base_file_directory = '/data/themis/'
	
	#: The base file URL 
	base_file_url = 'http://solarnet.oma.be/data/themis/'
	
	def get_relative_file_path(self):
		return self.file_path[13:]
	
	def get_oid(self):
		return self.field_values['date_obs'].strftime('%Y%m%d%H%M%S') + '_%04d' % self.field_values['wavelnth']
	
	def get_field_values(self):
		field_values = super(Record, self).get_field_values()
		
		field_values['date_beg'] = field_values['date_obs']
		field_values['date_end'] = parse_date(self.fits_header['DATE_END'])
		# TODO check if there is a better value
		field_values['wavemin'] = field_values['wavemax'] = field_values['wavelnth'] / 10.0
		return field_values

