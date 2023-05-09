from urllib.parse import unquote
from django.urls import reverse, NoReverseMatch
from django.db import connection
from django.db.models.constants import LOOKUP_SEP
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
			resource_uri = reverse('api_dispatch_list', kwargs={'resource_name': metadata_resource._meta.resource_name, 'api_name': metadata_resource._meta.api_name})
		except NoReverseMatch:
			return None
		
		# Create the query_string from the GET parameters
		# But remove the one about dataset filtering and also limit and offset
		excludes = ['name', 'description', 'instrument', 'telescope', 'characteristics', 'limit', 'offset', 'format']
		query_dict = bundle.request.GET.copy()
		for parameter in list(query_dict.keys()):
			try:
				field_name, trash = parameter.split(LOOKUP_SEP, 1)
			except ValueError:
				field_name = parameter
			if field_name in excludes:
				query_dict.pop(parameter)
		
		query_string = query_dict.urlencode()
		if query_string:
			resource_uri += '?' + query_string
		
		# Try to get an estimate of the metadata count, if the estimate is too small, use the excat count
		metadata_count = None
		
		# The estimate method use the statistics kept by postgresql about the tables, so cannot be used if there is a where clause
		if not query_dict:
			with connection.cursor() as cursor:
				cursor.execute('SELECT reltuples::bigint AS estimate FROM pg_class where relname = %s;', (metadata_model._meta.db_table,))
				estimated_count = cursor.fetchone()[0]
				if estimated_count > 1000:
					metadata_count = estimated_count
		
		if metadata_count is None:
			# Get the metadata query set corresponding to the query string to compute the exact count
			metadata = get_metadata_queryset(metadata_model, query_string, bundle.request.user)
			metadata_count = metadata.count()
		
		return {
			'resource_uri': resource_uri,
			'count': metadata_count
		}
	
	
	def get_via_uri(self, uri, request=None):
		'''Pull apart the salient bits of the URI and populates the resource via a obj_get'''
		# HACK: There is a BUG in tastypie which affect resource URI with spaces and special characteristics
		# the method get_resource_uri use django.urls.reverse to convert a ressource to it's URI
		# and reverse quotes the returned URI, but get_via_uri does not unquote it first
		return super().get_via_uri(unquote(uri), request)
