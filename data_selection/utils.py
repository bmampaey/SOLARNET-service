from zipfile import ZipFile
import requests
from django.conf import settings

from metadata.utils import get_metadata_queryset


__all__= ['DataSelectionZipIterator']


class DataSelectionZipIterator:
	'''Iterator that returns the files corresponding to data selections as one big zip file'''
	
	def __init__(self, data_selection):
		self.data_selection = data_selection
		self.missing_files = dict()
		self.total_file_size = 0
		
		# We cannot use a simple BytesIO because that would store all the files in memory
		# instead use a Pipe like buffer that destroy data when it is read
		self.zip_buffer = PipeLikeBuffer()
		self.zip_file = ZipFile(self.zip_buffer, 'w')
	
	def __iter__(self):
		'''Iterate over the files and return their zipped content'''
		for file_path, file_content in self.get_files():
			self.zip_file.writestr(file_path, file_content)
			yield self.zip_buffer.read()
		
		# Add a message about files that could not be included in the archive
		if self.missing_files:
			self.zip_file.writestr(settings.ZIP_ARCHIVE_MISSING_FILE_NAME, self.get_missing_files_content())
		
		# It is important to close the zip file because it writes some more data (central directory)
		self.zip_file.close()
		yield self.zip_buffer.read()
	
	def get_files(self):
		'''Generator that returns the file_path and file_content to be included in the ZIP archive'''
		# For each data location related to the metadata of the data selection, check if the file can be included in the ZIP archive
		# If so download the file and return it's content
		# Else add a message for the missing files to be included in the archive
		# Stop early if the total size of the files included in the zip archive is too large
		
		# Avoid processing files twice by keeping a list of the processed files
		processed_files = set()
		
		for file_path, file_url, file_size, offline in self.get_data_locations():
			
			if file_path in processed_files:
				continue
			else:
				processed_files.add(file_path)
			
			if offline:
				self.missing_files[file_path] = 'File is not accessible through the SVO, please contact the dataset manager to request access'
			
			elif file_size > settings.ZIP_ARCHIVE_MAX_FILE_SIZE:
				self.missing_files[file_path] = 'File is too large to be included in a ZIP archive, you can download it directly at %s or contact the dataset manager' % file_url
			
			elif self.total_file_size + file_size > settings.ZIP_ARCHIVE_MAX_SIZE:
				self.missing_files[settings.ZIP_ARCHIVE_TRUNCATED_WARNING] = ['Remaining files have not been included in the archive, for large data selection, please use FTP']
				return
			
			else:
				# TODO move this to an external utility with caching
				response = requests.get(file_url, timeout=50)
				if response.status_code in (200, 206):
					self.total_file_size += len(response.content)
					yield (file_path, response.content)
				else:
					self.missing_files[file_path] = 'Error while accessing the file, please retry or contact the dataset manager'
	
	def get_missing_files_content(self):
		'''Return the missing files as a text to be included in the ZIP archive'''
		return '\n'.join('%s: %s' % missing_file for missing_file in self.missing_files.items())
	
	def get_data_locations(self):
		'''Return the data location related to the metadata of the data selection'''
		# Return an iterator in case the data selection is huge
		return get_metadata_queryset(self.data_selection.dataset.metadata_model, self.data_selection.query_string, self.data_selection.owner).filter(data_location__isnull=False).values_list('data_location__file_path', 'data_location__file_url', 'data_location__file_size', 'data_location__offline').iterator()


class PipeLikeBuffer:
	'''Bytes buffer that acts like a pipe where read empty the buffer'''
	
	def __init__(self):
		self.buffer = b''
	
	def write(self, value):
		'''Add the value to the buffer and returns the number of bytes written'''
		self.buffer += value
		return len(value)
	
	def read(self):
		'''Return the value of the buffer and clear the buffer'''
		value = self.buffer
		self.buffer = b''
		return value
	
	def flush(self):
		# Necessary because called when closing the ZipFile
		pass
