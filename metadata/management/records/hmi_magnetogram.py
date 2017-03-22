from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from django.utils.timezone import utc
from metadata.management.records import FitsRecordFromDisk
from metadata.models import HmiMagnetogram

class Record(FitsRecordFromDisk):
	metadata_model = HmiMagnetogram
	exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax', 't_obs', 't_rec']
	hdu = 1
	
	#: The base directory in which are the files
	base_file_directory = '/data/SDO/'
	
	#: The base file URL 
	base_file_url = 'http://sdo.oma.be/data/'
	
	def get_relative_file_path(self):
		return self.file_path[40:]
	
	def get_thumbnail_url(self):
		return 'http://sdo.oma.be/PMD/preview_data/hmi_m_45s/{recnum}'.format(recnum = self.field_values['recnum'])
	
	def get_field_values(self):
		field_values = super(Record, self).get_field_values()
		
		# T_OBS T_REC are in TAI
		for field_name, keyword_name in [('t_obs', 'T_OBS'), ('t_rec', 'T_REC')]:
			try:
				field_values[field_name] = parse_date(self.fits_header[keyword_name].split('_')[0])
			except Exception, why:
					if not self.lax:
						raise
		
		field_values['date_beg'] = field_values['date_obs']
		# From fits file comment
		# DATE_OBS = T_OBS - EXPTIME/2.0
		# But T_OBS is in TAI and DATE_OBS is in UTC
		exptime = 2 * (field_values['t_obs'] - self.to_tai(field_values['date_obs']))
		field_values['date_end'] = field_values['date_beg'] + exptime
		# Taken from VSO
		field_values['wavemin'] = 6173 / 10.0
		field_values['wavemax'] = 6174 / 10.0
		return field_values
	
	def to_tai(self, utc):
		TAI_to_UTC = {
			datetime(2009, 1, 1, tzinfo = utc): timedelta(seconds=34),
			datetime(2012, 7, 1, tzinfo = utc): timedelta(seconds=35),
			datetime(2015, 7, 1, tzinfo = utc): timedelta(seconds=36),
			datetime(2017, 1, 1, tzinfo = utc): timedelta(seconds=37),
		}
		last_offset = max(date for date in TAI_to_UTC if utc >= date)
		return (utc + TAI_to_UTC[last_offset]).replace(tzinfo=None)