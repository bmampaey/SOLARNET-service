from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404

from dataset.models import Dataset

class Data(RedirectView):
	'''View to download the data by looking up it's dataset id and metadata oid'''
	# TODO allow to download by oid or using filter (see django_filter), if there is more than one gives back the first one
	http_method_names = ['get', 'head']
	permanent = True
	
	def get_redirect_url(self, dataset_id, metadata_oid):
		dataset = get_object_or_404(Dataset, id=dataset_id)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.file_url

class Thumbnail(RedirectView):
	'''View to download the thumbnail by looking up it's dataset id and metadata oid'''
	# TODO allow to download by oid or using filter (see django_filter), if there is more than one gives back the first one
	http_method_names = ['get', 'head']
	permanent = True
	
	def get_redirect_url(self, dataset_id, metadata_oid):
		dataset = get_object_or_404(Dataset, id=dataset_id)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.thumbnail_url
