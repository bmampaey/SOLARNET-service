from dataset.management.populate import PopulatorForVSO

class Populator(PopulatorForVSO):
	header_size = 5760
	zipped = True
	instrument = 'ChroTel'
	dataset_id = 'chrotel'
	
	def get_field_values(self, fields, header):
		field_values = super(Populator, self).get_field_values(fields, header)
		
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