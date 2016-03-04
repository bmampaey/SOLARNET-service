from dataset.management.populate import PopulatorForFiles

class Populator(PopulatorForFiles):
	dataset = 'eit'
	directory = '/data/soho-archive/eit/lz'
	file_url_template = 'http://sidc.be/eitlz/{year}/{month}/{filename}'
	thumbnail_url_template = None
	
	def get_oid(self, header):
		'''Return the oid for the record'''
		return parse_date(header['DATE_OBS']).strftime('%Y%m%d%H%M%s')
	
	def get_field_values(self, fields, header):
		field_values = super(Populator, self).get_field_values(fields, header)
		field_values['date_beg'] = field_values['date_obs']
		field_values['date_end'] = field_values['date_obs'] + field_values['exptime']
		# TODO check if there is a better value
		field_values['wavemin'] = field_values['wavemax'] = field_values['wavelnth']
		return field_values