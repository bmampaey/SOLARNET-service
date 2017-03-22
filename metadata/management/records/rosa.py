import re
from datetime import timedelta, datetime
from django.utils.timezone import utc
from metadata.management.records import FitsRecordFromHTTP
from metadata.models import Rosa

class Record(FitsRecordFromHTTP):
	metadata_model = Rosa
	exclude_fields = []
	zipped = False
	
	# See https://star.pst.qub.ac.uk/webdav/public/fchroma/2014-10-25/25Oct2014%20%E2%80%93%20Main%20Data%20Properties.pdf
	
	data_properties = {
		'1sttarget': {
			'DATE-BEG': datetime(2014, 10, 25, 15, 9, 0, tzinfo=utc),
			'OBSRVTRY': 'NSO Sacramento Peak',
			'TELESCOP': 'Dunn Solar Telescope',
			'INSTRUME': 'ROSA',
			'POINTING': 'S14.8, W23.9',
			'TARGET': 'AR 12192',
			'GOES_CLS': 'X1.0',
			'CHANNEL': {
				'Continuum3500': {'WAVELNTH': 3500, 'CADENCE': 4.577, 'XPOSURE': 0.1},
				'Continuum4170': {'WAVELNTH': 4170, 'CADENCE': 2.112, 'XPOSURE': 0.018},
				'Gband': {'WAVELNTH': 4300, 'CADENCE': 2.112, 'XPOSURE': 0.017},
			},
		},
		'2ndtarget': {
			'DATE-BEG': datetime(2014, 10, 25, 16, 7, 32, tzinfo=utc),
			'OBSRVTRY': 'NSO Sacramento Peak',
			'TELESCOP': 'Dunn Solar Telescope',
			'INSTRUME': 'ROSA',
			'POINTING': 'S14.4, W28.5',
			'TARGET': 'AR 12192',
			'GOES_CLS': 'X1.0',
			'CHANNEL': {
				'Continuum3500': {'WAVELNTH': 3500, 'CADENCE': 4.577, 'XPOSURE': 0.1},
				'Continuum4170': {'WAVELNTH': 4170, 'CADENCE': 2.112, 'XPOSURE': 0.018},
				'Gband': {'WAVELNTH': 4300, 'CADENCE': 2.112, 'XPOSURE': 0.017},
			},
		}
	}
	
	def get_oid(self):
		return self.field_values['date_beg'].strftime('%Y%m%d%H%M%S%f') + '_%04d' % self.field_values['wavelnth']
	
	def get_relative_file_path(self):
		return self.file_url[49:]
	
	def get_file_number(self):
		match = re.match('.*/file_(?P<number>\d+).fits$', self.relative_file_path)
		if match:
			return int(match.group('number'))
		else:
			raise ValueError('Could not find file number of %s' % self.file_url)
	
	def get_fits_header(self):
		# There is nothing in ROSA fits header, so we fill the header artificially
		fits_header = super(Record, self).get_fits_header()
		
		# Find target and channel
		target = next(target for target in self.data_properties if target in self.relative_file_path)
		channel = next(channel for channel in self.data_properties[target]['CHANNEL'] if channel in self.relative_file_path)
		
		# Set regular keywords
		for keyword in 'OBSRVTRY', 'TELESCOP', 'INSTRUME', 'POINTING', 'TARGET', 'GOES_CLS':
			fits_header[keyword] = self.data_properties[target][keyword]
		fits_header['CHANNEL'] = channel
		fits_header['WAVELNTH'] = self.data_properties[target]['CHANNEL'][channel]['WAVELNTH']
		fits_header['CADENCE'] = self.data_properties[target]['CHANNEL'][channel]['CADENCE']
		fits_header['XPOSURE'] = self.data_properties[target]['CHANNEL'][channel]['XPOSURE']
		
		# Set special keywords
		start_date = self.data_properties[target]['DATE-BEG'] + timedelta(seconds=self.file_number * self.data_properties[target]['CHANNEL'][channel]['CADENCE'])
		end_date = start_date + timedelta(seconds=self.data_properties[target]['CHANNEL'][channel]['XPOSURE'])
		fits_header['DATE-BEG'] = start_date.isoformat()
		fits_header['DATE-END'] = end_date.isoformat()
		fits_header['WAVEMIN'] = fits_header['WAVELNTH'] / 10.
		fits_header['WAVEMAX'] = fits_header['WAVELNTH'] / 10.
		
		return fits_header

