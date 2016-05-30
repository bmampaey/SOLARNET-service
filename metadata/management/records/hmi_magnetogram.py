from datetime import datetime, timedelta
import pytz
from dateutil.parser import parse as parse_date

from metadata.management import records
from metadata.models import HmiMagnetogram

class RecordFromFitsFile(records.RecordFromFitsFile):
	'''Record created from a Fist file on disk'''
	
	metadata_model = HmiMagnetogram
	exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax', 't_obs', 't_rec']
	HDU = 1
	
	#: The base directory in which are the files
	base_file_directory = '/data/SDO/'
	
	#: The base file URL 
	base_file_url = 'http://sdo.oma.be/data/'
	
	def get_thumbnail_url(self):
		return 'http://sdo.oma.be/PMD/preview_data/hmi_m_45s/{recnum}'.format(recnum = self.field_values['recnum'])
	
	def get_field_values(self):
		field_values = super(RecordFromFitsFile, self).get_field_values()
		
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
			datetime(2009, 1, 1, tzinfo = pytz.UTC): timedelta(seconds=34),
			datetime(2012, 7, 1, tzinfo = pytz.UTC): timedelta(seconds=35),
			datetime(2015, 7, 1, tzinfo = pytz.UTC): timedelta(seconds=36),
		}
		last_offset = max(date for date in TAI_to_UTC if utc >= date)
		return (utc + TAI_to_UTC[last_offset]).replace(tzinfo=None)