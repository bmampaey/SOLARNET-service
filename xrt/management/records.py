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
		import pdb; pdb.set_trace()
		field_values = super(RecordFromVSO, self).get_field_values()
		
		# See https://xrt.cfa.harvard.edu/resources/documents/XAG/XAG.pdf
		field_values['date_beg'] = field_values['date_obs']
		full_width_at_half_maximum = 17
		field_values['wavemin'] = 430.5 - full_width_at_half_maximum
		field_values['wavemax'] = 430.5 + full_width_at_half_maximum
		
		return field_values