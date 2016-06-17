import os, zipfile, urllib2
from cStringIO import StringIO
from django.views.generic.detail import SingleObjectMixin
from django_downloadview import VirtualDownloadView, VirtualFile, BytesIteratorIO

from data_selection.models import DataSelectionGroup, DataSelection

#https://code.djangoproject.com/wiki/CookBookDynamicZip
#http://chase-seibert.github.io/blog/2010/07/23/django-zip-files-create-dynamic-in-memory-archives-with-pythons-zipfile.html
 # fix for Linux zip files read in Windows
 #   for file in zip.filelist:
 #	   file.create_system = 0  

def ZIP(data_selections):
	'''Generator that returns a data selection as a zip file'''
	data_selections = data_selections
	buffer = StringIO()
	zip_file = zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, allowZip64 = True)
	for data_selection in data_selections:
		for data_location in data_selection.metadata.values('data_location__file_path', 'data_location__file_url'):
			file_name = os.path.join(data_selection.dataset.name, data_location['data_location__file_path'])
			request = urllib2.urlopen(data_location['data_location__file_url'])
			zip_file.writestr(file_name, request.read())
			buffer.flush()
			buffer.seek(0)
			yield buffer.read()
	
	# it is important to close the files as it writes some more data to the file
	# and to send also that data
	zip_file.close()
	buffer.flush()
	buffer.seek(0)
	yield buffer.read()

class DownloadDataSelectionGroupView(SingleObjectMixin, VirtualDownloadView):
	'''See http://django-downloadview.readthedocs.org/'''
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
	'''See http://django-downloadview.readthedocs.org/'''
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
