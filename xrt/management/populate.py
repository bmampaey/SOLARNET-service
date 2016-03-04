from dataset.management.populate import PopulatorForVSO

class Populator(PopulatorForVSO):
	instrument='XRT'
	header_size = 20160
	zipped = False
	dataset_id = 'xrt'
	
	def get_field_values(self, fields, header):
		field_values = super(Populator, self).get_field_values(fields, header)
		
		# See https://xrt.cfa.harvard.edu/resources/documents/XAG/XAG.pdf
		field_values['date_beg'] = field_values['date_obs']
		full_width_at_half_maximum = 17
		field_values['wavemin'] = 430.5 - full_width_at_half_maximum
		field_values['wavemax'] = 430.5 + full_width_at_half_maximum
		
		return field_values