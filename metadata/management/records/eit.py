import os
from dateutil.parser import parse as parse_date
from datetime import timedelta

from metadata.management import records
from metadata.models import Eit

class RecordFromFitsFile(records.RecordFromFitsFile):
	'''Record created from a Fist file on disk'''
	
	metadata_model = Eit
	exclude_fields = ['date_beg', 'date_end', 'wavemin', 'wavemax', 'blocks_horz', 'blocks_vert', 'image_of_seq', 'n_missing_blocks', 'num_leb_proc', 'camera_err', 'line_sync', 'readout_port', 'shutter_close_time', 'commanded_exposure_time', 'corrected_date_obs', 'leb_proc']
	HDU = 0
	
	#: The base directory in which are the files
	base_file_directory = '/data/soho-archive/eit/lz/'
	
	#: The base file URL 
	base_file_url = 'http://sidc.be/eitlz/'	
	
	def get_relative_file_path(self):
		return self.file_path[26:]
	
	def get_file_url(self):
		file_abspath = os.path.abspath(self.file_path)
		if not file_abspath.startswith(self.base_file_directory):
			raise ValueError('File path is not in directory %s: check base_file_directory' % self.base_file_directory)
	
		file_relpath = file_abspath[len(self.base_file_directory):]
		if file_relpath.startswith('/') and self.base_file_url.endswith('/'):
			file_relpath = file_relpath[:-1]
		return self.base_file_url + file_relpath
	
	def get_field_values(self):
		
		field_values = super(RecordFromFitsFile, self).get_field_values()
		
		# EIT has additional keywords in comments
		comments = dict()
		for comment in self.fits_header['COMMENT']:
		 	try:
		 		key, value = comment.split('=', 1)
		 	except ValueError:
		 		pass
		 	else:
		 		comments[key.lower().strip().replace(' ', '_')] = value.strip()
		
		for key in 'blocks_horz', 'blocks_vert', 'image_of_seq', 'n_missing_blocks', 'num_leb_proc':
			try:
				field_values[key] = int(comments[key])
			except (ValueError, KeyError):
				if not self.lax:
					raise
			
		for key in 'shutter_close_time', 'commanded_exposure_time':
			try:
				values = comments[key].split()
				field_values[key] = float(values[0])
			except (KeyError, ValueError):
				if not self.lax:
					raise
		
		for key in 'camera_err', 'line_sync', 'readout_port':
			try:
				field_values[key] = comments[key]
			except KeyError:
				if not self.lax:
					raise
		try:
			field_values['corrected_date_obs'] = parse_date(comments['corrected_date_obs'])
		except (ValueError, KeyError):
			if not self.lax:
				raise
		
		if 'exptime' not in field_values:
			field_values['exptime'] = field_values['commanded_exposure_time'] + field_values['shutter_close_time']
		
		field_values['date_beg'] = field_values['corrected_date_obs']
		field_values['date_end'] = field_values['date_beg'] + timedelta(seconds=field_values['exptime'])
		# TODO check if there is a better value
		field_values['wavemin'] = field_values['wavemax'] = field_values['wavelnth'] / 10.0
		return field_values