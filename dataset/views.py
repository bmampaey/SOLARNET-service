from django.views.generic import RedirectView, View
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from PIL import Image
import requests


from dataset.models import Dataset

__all__ = ['DataView', 'ThumbnailView', 'Image2ThumbnailView']

# TODO allow to download by oid or using filter (see django_filter), if there is more than one gives back the first one
# TODO should we check online flag ?
class DataView(RedirectView):
	'''View to download the data by looking up the metadata resource name and oid'''
	http_method_names = ['get', 'head']
	
	def get_redirect_url(self, dataset_name, metadata_oid):
		dataset = get_object_or_404(Dataset, name=dataset_name)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.file_url


class ThumbnailView(RedirectView):
	'''View to download the thumbnail by looking up the metadata resource name and metadata oid'''
	http_method_names = ['get', 'head']
	
	def get_redirect_url(self, dataset_name, metadata_oid):
		dataset = get_object_or_404(Dataset, name=dataset_name)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.thumbnail_url

class Image2ThumbnailView(View):
	'''View to convert an image to a thumbnail'''
	
	def get(self, request, *args, **kwargs):
		'''Return a response with the thumbnail'''
		try:
			image = Image.open(requests.get(request.GET['url'], stream=True).raw)
			image.thumbnail((512,512))
			thumbnail = ContentFile(b'', name='thumbnail.jpg')
			image.save(thumbnail, format='jpeg')
			thumbnail.seek(0)
		except Exception as why:
			raise Http404 from why
		return FileResponse(thumbnail)
