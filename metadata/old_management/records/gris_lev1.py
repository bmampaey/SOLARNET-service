from datetime import datetime, time
from requests.auth import HTTPDigestAuth
from django.utils.dateparse import parse_time
from django.utils.timezone import utc
from metadata.management.records import FitsRecordFromHTTP
from metadata.models import GrisLev1

class Record(FitsRecordFromHTTP):
	metadata_model = GrisLev1
	exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax']
	min_header_size = 118080
	zipped = False
	auth =  HTTPDigestAuth('gris', 'grausam')
	
	def get_relative_file_path(self):
		return self.file_url[39:]
	
	def get_field_values(self):
		field_values = super(Record, self).get_field_values()
		
		min_time, max_time = time.max, time.min
		for card in self.fits_header.cards:
			try:
				card.verify('silentfix')
			except Exception as why:
				self.log.warning('Bad card in header %s: %s', card, why)
				continue
			if card.keyword.lower() == 'ut':
				try:
					ut = parse_time(card.value)
				except ValueError as why:
					self.log.warning('UT keyword has a ill formated value %s: %s', card.value, why)
				else:
					min_time = min(min_time, ut)
					max_time = max(max_time, ut)
		
		field_values['date_beg'] = datetime.combine(field_values['date_obs'], min_time.replace(tzinfo=utc))
		field_values['date_end'] = datetime.combine(field_values['date_obs'], max_time.replace(tzinfo=utc))
		field_values['wavemin'] = field_values['waveleng']
		field_values['wavemax'] = field_values['waveleng']
		
		return field_values
