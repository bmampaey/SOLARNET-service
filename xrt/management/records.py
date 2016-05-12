from datetime import timedelta

from dataset.management import records
from ..models import Metadata

class RecordFromVSO(records.RecordFromVSO):
	metadata_model = Metadata
	exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax']
	instrument = 'XRT'
	min_header_size = 20160
	zipped = False
	
	def get_file_url(self):
		return self.vso_record.fileid
		
	def get_field_values(self):
		field_values = super(RecordFromVSO, self).get_field_values()
		
		# See https://xrt.cfa.harvard.edu/resources/documents/XAG/XAG.pdf
		field_values['date_beg'] = field_values['date_obs']
		# from VSO
		field_values['wavemin'] = 0.88
		field_values['wavemax'] = 33.5
		
		return field_values
