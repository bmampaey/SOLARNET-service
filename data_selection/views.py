import os, zipfile, requests
from django.views.generic.detail import SingleObjectMixin
from django_downloadview import VirtualDownloadView, VirtualFile, BytesIteratorIO

from data_selection.models import DataSelectionGroup, DataSelection

class AppendOnlyFile:
	'''Fake file that can only be appended to'''
	def __init__(self):
		self.buffer= b''
		self.pos = 0
	
	def tell(self):
		return self.pos
	
	def seek(self):
		raise BufferError('Cannot seek on append only file')
	
	def write(self, value):
		self.buffer += value
		self.pos += len(value)
	
	def read(self):
		return self.buffer
	
	def flush(self):
		pass
	
	def clear(self):
		self.buffer = b''
	
	def close(self):
		self.buffer = b''
		self.pos = 0

def ZIP(data_selections):
	'''Generator that returns data selections as a zip file'''
	data_selections = data_selections
	zip_buffer = AppendOnlyFile()
	zip_file = zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, allowZip64 = True)
	missing_files = ''
	for data_selection in data_selections:
		for data_location in data_selection.metadata.values('data_location__file_path', 'data_location__file_url', 'data_location__offline', 'data_location__file_size'):
			file_name = os.path.join(data_selection.dataset.name, data_location['data_location__file_path'])
			
			if data_location['data_location__offline']:
				missing_files += file_name + ' is not accessible online, please contact dataset manager\n'
			# TODO increase server memory size
			elif data_location['data_location__file_size'] > 100 * 1024 * 1024:
				missing_files += file_name + ' is too large, please use FTP\n'
			else:
				response = requests.get(data_location['data_location__file_url'], timeout=50)
				if response.status_code in (200, 206):
					zip_file.writestr(file_name, response.content)
					yield zip_buffer.read()
				else:
					missing_files += file_name + ' error downloading, please retry or contact dataset manager\n'
			
			# clear the buffer before next writing
			zip_buffer.clear()
	
	# Add the missing files
	if missing_files:
		zip_file.writestr('missing_files.txt', missing_files)
	
	# it is important to close the files as it writes some more data (central directory) to the file
	# and to send also that data
	zip_file.close()
	yield zip_buffer.read()

class DownloadDataSelectionGroupView(SingleObjectMixin, VirtualDownloadView):
	'''View to download a zip archive of a data selection group'''
	attachment = True
	mimetype = 'application/zip'
	model = DataSelectionGroup
	
	def get_file(self):
		'''Return wrapper on BytesIteratorIO object.'''
		self.object = self.get_object()
		file_obj = BytesIteratorIO(ZIP(self.object.data_selections.all()))
		virtual_file = VirtualFile(file_obj, name = self.object.name.replace(' ', '_') + '.zip')
		# hack because of bug in VirtualFile
		virtual_file._size = None
		return virtual_file

class DownloadDataSelectionView(SingleObjectMixin, VirtualDownloadView):
	'''View to download a zip archive of a data selection'''
	attachment = True
	mimetype = 'application/zip'
	model = DataSelection
	
	def get_file(self):
		'''Return wrapper on BytesIteratorIO object.'''
		self.object = self.get_object()
		file_obj = BytesIteratorIO(ZIP([self.object]))
		virtual_file = VirtualFile(file_obj, name = self.object.data_selection_group.name.replace(' ', '_') + '.zip')
		# hack because of bug in VirtualFile
		virtual_file._size = None
		return virtual_file
