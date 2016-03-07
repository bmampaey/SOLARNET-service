from dataset.management.populate import PopulatorForFiles
from dateutil.parser import parse as parse_date
import os
from itertools import chain
from glob import glob
from dateutil import rrule
from datetime import datetime, timedelta

class Populator(PopulatorForFiles):
	dataset_id = 'eit'
	directory = '/data/soho-archive/eit/lz/'
	file_pattern = 'efz*'
	file_url_template = 'http://sidc.be/eitlz/'
	thumbnail_url_template = None
	skip_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax', 'blocks_horz', 'blocks_vert', 'image_of_seq', 'n_missing_blocks', 'num_leb_proc', 'camera_err', 'line_sync', 'readout_port', 'shutter_close_time', 'commanded_exposure_time', 'corrected_date_obs', 'leb_proc']
	
	def get_oid(self, header):
		'''Return the oid for the record'''
		return int(parse_date(header['DATE_OBS']).strftime('%Y%m%d%H%M%S'))
	
	def get_file_url(self, header, file_path):
		'''Return the file url for the record'''
		return self.file_url_template + file_path[len(self.directory):]
	
	def list_files(self, start_date = None, end_date = None):
		if start_date is None:
			return super(Populator, self).list_files(start_date, end_date)
		else:
			return chain.from_iterable(glob(os.path.join(self.directory, '%04d'%x.year, '%02d'%x.month, self.file_pattern)) for x in rrule.rrule(rrule.MONTHLY, dtstart=start_date.replace(day=1), until=end_date or datetime.now()))
	
	def get_field_values(self, fields, header):
		import pdb; pdb.set_trace()
		field_values = super(Populator, self).get_field_values(fields, header)
		
		# EIT has additional keywords in comments
		comments = dict()
		for comment in header['COMMENT']:
		 	try:
		 		key, value = comment.split('=', 1)
		 	except ValueError:
		 		pass
		 	else:
		 		comments[key.lower().strip().replace(' ', '_')] = value.strip()
		
		for key in 'blocks_horz', 'blocks_vert', 'image_of_seq', 'n_missing_blocks', 'num_leb_proc':
			try:
				field_values[key] = int(comments[key])
			except KeyError:
				self.log.warning('Missing keyword %s in header comments', key)
			except ValueError:
				self.log.warning('Value for keyword %s is not of type int: %s', key, comments[key])
		
		for key in 'camera_err', 'line_sync', 'readout_port', 'shutter_close_time', 'commanded_exposure_time':
			try:
				field_values[key] = comments[key]
			except KeyError:
				self.log.warning('Missing keyword %s in header comments', key)
		
		try:
			field_values['corrected_date_obs'] = parse_date(comments['corrected_date_obs'])
		except KeyError:
			self.log.warning('Missing keyword %s in header comments', key)
		except ValueError:
			self.log.warning('Value for keyword %s cannot be converted to datetime: %s', key, comments[key])
		
		field_values['date_beg'] = field_values['date_obs']
		field_values['date_end'] = field_values['date_obs'] + timedelta(seconds=field_values['exptime'])
		# TODO check if there is a better value
		field_values['wavemin'] = field_values['wavemax'] = field_values['wavelnth']
		return field_values