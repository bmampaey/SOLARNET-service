from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404

from dataset.models import Dataset

__all__ = ['DataView', 'ThumbnailView']

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
