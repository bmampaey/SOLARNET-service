import os, zipfile, urllib2
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
	buffer = AppendOnlyFile()
	zip_file = zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, allowZip64 = True)
	for data_selection in data_selections:
		for data_location in data_selection.metadata.values('data_location__file_path', 'data_location__file_url'):
			file_name = os.path.join(data_selection.dataset.name, data_location['data_location__file_path'])
			request = urllib2.urlopen(data_location['data_location__file_url'])
			# clear the buffer before writting
			buffer.clear()
			zip_file.writestr(file_name, request.read())
			yield buffer.read()
	
	# it is important to close the files as it writes some more data (central directory) to the file
	# and to send also that data
	buffer.clear()
	zip_file.close()
	yield buffer.read()

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
