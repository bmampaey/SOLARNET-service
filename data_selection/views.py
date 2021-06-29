from urllib.parse import quote
from django.views.generic.detail import SingleObjectMixin, View
from django.http import StreamingHttpResponse

from data_selection.models import DataSelection
from data_selection.utils import DataSelectionZipIterator

__all__ = ['DataSelectionDownloadZipView']


class DataSelectionDownloadZipView(SingleObjectMixin, View):
	'''View to download a zip archive of a data selection'''
	model = DataSelection
	slug_field = 'uuid'
	slug_url_kwarg = 'uuid'
	
	def get(self, request, *args, **kwargs):
		'''Return wrapper on BytesIteratorIO object.'''
		self.object = self.get_object()
		file_iterator = DataSelectionZipIterator(self.object)
		file_name = quote(self.object.zip_file_name)
		return StreamingHttpResponse(file_iterator, content_type = 'application/zip', headers={'Content-Disposition': 'attachment; filename*=utf-8\'\''+file_name})
