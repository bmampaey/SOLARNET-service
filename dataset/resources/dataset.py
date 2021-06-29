from urllib.parse import unquote
from django.urls import reverse, NoReverseMatch
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.exceptions import NotRegistered

from api.constants import FILTERS
from dataset.models import Dataset
from metadata.utils import get_metadata_queryset
from .meta import ResourceMeta

__all__ = ['DatasetResource']

class DatasetResource(ModelResource):
	'''RESTful resource for model Dataset'''
	
	telescope = fields.ToOneField('dataset.resources.TelescopeResource', 'telescope', full=True)
	instrument = fields.ToOneField('dataset.resources.InstrumentResource', 'instrument', full=True)
	characteristics = fields.ToManyField('dataset.resources.CharacteristicResource', 'characteristics', full=True)
	# Object containing the metadata resource URI with an appropriate query string and the estimated number of items that would be returned if fetching that URI
	metadata = fields.DictField(readonly=True, help_text = 'The URI and the estimated count for the metadata of the dataset with current filters applied')
	
	class Meta(ResourceMeta):
		queryset = Dataset.objects.all()
		resource_name = 'dataset'
		# Make the URI for dataset the name instead of the id
		detail_uri_name = 'name'
		# Don't leak emails and user_group, metadata_content_type is replaced by the metadata DictField above
		excludes = ['id', 'contact_email', 'user_group', 'metadata_content_type']
		filtering = {
			'name': FILTERS.TEXT,
			'description': FILTERS.TEXT,
			'telescope': FILTERS.RELATIONAL,
			'instrument': FILTERS.RELATIONAL,
			'characteristics': FILTERS.RELATIONAL
		}
		ordering = ['name', 'description', 'telescope', 'instrument', 'characteristics']
	
	def apply_filters(self, request, applicable_filters):
		'''Apply the filters to the object list'''
		
		# Avoid duplicate results when filtering on relations
		return super().apply_filters(request, applicable_filters).distinct()
	
	def dehydrate_metadata(self, bundle):
		'''Return the value for the metadata DictField'''
		
		# Get the metadata model and the corrresponding resource for the dataset
		try:
			metadata_model = bundle.obj.metadata_model
		except ValueError:
			return None
		
		try:
			metadata_resource = self._meta.api.canonical_resource_for(metadata_model)
		except NotRegistered:
			return None
		
		# Get the URI of the metadata resource and add the query string
		try:
			uri = reverse('api_dispatch_list', kwargs={'resource_name': metadata_resource._meta.resource_name, 'api_name': metadata_resource._meta.api_name})
		except NoReverseMatch:
			return None
		
		query_string = bundle.request.GET.urlencode()
		if query_string:
			uri += '?' + query_string
		
		# Get the metadata query set corresponding to the query string to compute the estimated count
		metadata = get_metadata_queryset(metadata_model, query_string, bundle.request.user)
		
		return {
			'uri': uri,
			'estimated_count': metadata.estimated_count()
		}
	
	def get_via_uri(self, uri, request=None):
		'''Pull apart the salient bits of the URI and populates the resource via a obj_get'''
		# HACK: There is a BUG in tastypie which affect resource URI with spaces and special characteristics
		# the method get_resource_uri use django.urls.reverse to convert a ressource to it's URI
		# and reverse quotes the returned URI, but get_via_uri does not unquote it first
		return super().get_via_uri(unquote(uri), request)
