from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404
from dataset.models import Dataset

class DownloadData(RedirectView):
	'''View to download the data by looking up it's dataset id and metadata oid'''
	http_method_names = [u'get', u'head']
	permanent = True
	
	def get_redirect_url(self, dataset_id, metadata_oid):
		dataset = get_object_or_404(Dataset, id=dataset_id)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.url
