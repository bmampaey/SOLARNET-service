from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404
from django.core.exceptions import ImproperlyConfigured


from rest_framework import viewsets
from rest_framework.settings import api_settings
from rest_framework.filters import OrderingFilter
from rest_framework import serializers

from dataset.models import Telescope, Instrument, Characteristic, Dataset, Keyword, DataLocation, Tag
from dataset.serializers import TelescopeSerializer, InstrumentSerializer, DatasetSerializer, CharacteristicSerializer, KeywordSerializer, DataLocationSerializer, TagSerializer
from dataset.filters import MetadataFilterBackend, DatasetFilter

class DownloadData(RedirectView):
	'''View to download the data by looking up it's dataset id and metadata oid'''
	# TODO allow to download by oid or using filter (see django_filter), if there is more than one gives back the first one
	http_method_names = [u'get', u'head']
	permanent = True
	
	def get_redirect_url(self, dataset_id, metadata_oid):
		import pdb; pdb.set_trace()
		dataset = get_object_or_404(Dataset, id=dataset_id)
		metadata = get_object_or_404(dataset.metadata_model, oid=metadata_oid)
		return metadata.data_location.url

class TelescopeViewSet(viewsets.ReadOnlyModelViewSet):
	'''API endpoint that allows telescopes to be viewed or edited.'''
	queryset = Telescope.objects.all()
	serializer_class = TelescopeSerializer


class InstrumentViewSet(viewsets.ReadOnlyModelViewSet):
	'''API endpoint that allows instruments to be viewed or edited.'''
	queryset = Instrument.objects.all()
	serializer_class = InstrumentSerializer


class DataLocationViewSet(viewsets.ReadOnlyModelViewSet):
	'''API endpoint that allows data locations to be viewed or edited.'''
	queryset = DataLocation.objects.all()
	serializer_class = DataLocationSerializer

class KeywordViewSet(viewsets.ReadOnlyModelViewSet):
	'''API endpoint that allows keywords to be viewed or edited.'''
	queryset = Keyword.objects.all()
	serializer_class = KeywordSerializer


class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
	'''API endpoint that allows datasets to be viewed or edited.'''
	queryset = Dataset.objects.all()
	serializer_class = DatasetSerializer
	filter_class = DatasetFilter

class CharacteristicViewSet(viewsets.ReadOnlyModelViewSet):
	'''API endpoint that allows characteristics to be viewed or edited.'''
	queryset = Characteristic.objects.all()
	serializer_class = CharacteristicSerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):
	''' API endpoint that allows tags to be viewed or edited.'''
	
	queryset = Tag.objects.all()
	serializer_class = TagSerializer

class BaseMetadataViewSet(viewsets.ReadOnlyModelViewSet):
	'''API endpoint that allows metadata to be viewed or edited. '''
	
	lookup_field = 'oid'
	filter_backends = [MetadataFilterBackend, OrderingFilter]
	
	def get_queryset(self):
		'''Returns the queryset or set create one if it hasn't been set'''
		
		if getattr(self, 'queryset') is not None:
			return super(BaseMetadataViewSet, self).get_queryset()
		elif not hasattr(self, 'model'):
			raise ImproperlyConfigured('%s is missing a model. Define a model or a queryset, or override get_queryset' % self.__class__.name)
		else:
			return self.model.objects.all()
	
	def get_serializer_class(self):
		'''Returns the serializer class or create a default one if it hasn't been set'''
		
		if getattr(self, 'serializer_class') is not None:
			return super(BaseMetadataViewSet, self).get_serializer_class()
		
		class MetadataSerializer(serializers.HyperlinkedModelSerializer):
			data_location = DataLocationSerializer()
			
			class Meta:
				model = self.get_queryset().model
				extra_kwargs = {'uri': {'lookup_field': 'oid', 'view_name': model._meta.app_label + '-detail'}}
		
		return MetadataSerializer