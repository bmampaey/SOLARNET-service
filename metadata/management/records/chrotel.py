from datetime import timedelta
from urlparse import urlparse

from metadata.management import records
from metadata.models import Chrotel

class RecordFromVSO(records.RecordFromVSO):
	metadata_model = Chrotel
	exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax']
	instrument = 'ChroTel'
	min_header_size = 5760
	zipped = True
	
	def get_header_file_url(self):
		return urlparse(self.vso_record.fileid)._replace(scheme='http').geturl()
	
	def get_relative_file_path(self):
		return self.file_url[103:]
	
	def get_field_values(self):
		field_values = super(RecordFromVSO, self).get_field_values()
		
		# See http://www.kis.uni-freiburg.de/en/observatories/chrotel/data/
		field_values['date_beg'] = field_values['date_obs']
		field_values['date_end'] = field_values['date_obs'] + timedelta(seconds = field_values['exptime'])
		full_width_at_half_maximum = {
			393.4 : 0.03,
			656.2 : 0.05,
			1083.0: 0.14
		}
		field_values['wavemin'] = field_values['wavelnth'] - full_width_at_half_maximum[field_values['wavelnth']]
		field_values['wavemax'] = field_values['wavelnth'] + full_width_at_half_maximum[field_values['wavelnth']]
		
		return field_values
