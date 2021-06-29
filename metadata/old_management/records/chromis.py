from dateutil.parser import parse as parse_date
from metadata.management.records import FitsRecordFromDisk
from metadata.models import Chromis

class Record(FitsRecordFromDisk):
	metadata_model = Chromis
	#exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax']
	
	#: The base directory in which are the files
	base_file_directory = '/tmp/'
	
	#: The base file URL
	base_file_url = 'https://www.isf.astro.su.se/'
	
	def get_relative_file_path(self):
		return self.file_path[len(self.base_file_directory):]
	
	def get_oid(self):
		return parse_date(self.fits_header['DATE-OBS']).strftime('%Y%m%d%H%M%S')
