from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from dataset.models import Telescope, Instrument, Characteristic, Dataset, Keyword
from dataset.models import DataLocation, Tag

from dataset.serializers import TelescopeSerializer, InstrumentSerializer, DatasetSerializer, CharacteristicSerializer, KeywordSerializer, DataLocationSerializer, TagSerializer

class DownloadData(RedirectView):
	'''View to download the data by looking up it's dataset id and metadata oid'''
	http_method_names = [u'get', u'head']
	permanent = True
	
	def get_redirect_url(self, dataset_id, metadata_oid):
		import pdb; pdb.set_trace()
		dataset = get_object_or_404(Dataset, id=dataset_id)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.url

class TelescopeViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows telescopes to be viewed or edited.
	"""
	queryset = Telescope.objects.all()
	serializer_class = TelescopeSerializer


class InstrumentViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows instruments to be viewed or edited.
	"""
	queryset = Instrument.objects.all()
	serializer_class = InstrumentSerializer


class DataLocationViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows data locations to be viewed or edited.
	"""
	queryset = DataLocation.objects.all()
	serializer_class = DataLocationSerializer

class KeywordViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows keywords to be viewed or edited.
	"""
	queryset = Keyword.objects.all()
	serializer_class = KeywordSerializer

class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows datasets to be viewed or edited.
	"""
	queryset = Dataset.objects.all()
	serializer_class = DatasetSerializer

class CharacteristicViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows characteristics to be viewed or edited.
	"""
	queryset = Characteristic.objects.all()
	serializer_class = CharacteristicSerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows tags to be viewed or edited.
	"""
	queryset = Tag.objects.all()
	serializer_class = TagSerializer