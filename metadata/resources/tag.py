from urllib.parse import unquote
from django.forms import modelform_factory
from tastypie.validation import FormValidation
from tastypie.resources import ModelResource
from tastypie.cache import SimpleCache

from api.authentications import ApiKeyOrAnonymousAuthentication
from api.authorizations import AlwaysReadAuthorization
from api.serializers import Serializer
from api.constants import FILTERS
from dataset.models import Dataset
from metadata.models import Tag

__all__ = ['TagResource']

class TagResource(ModelResource):
	'''RESTful resource for model Tag'''
	
	class Meta:
		# Allow only methods corresponding to create/read on the list URL and read on the detail URL
		list_allowed_methods = ['post', 'get']
		detail_allowed_methods = ['get']
		# When requesting to create/update 1 or more objects, return the objects in the response
		always_return_data = True
		authentication = ApiKeyOrAnonymousAuthentication()
		authorization = AlwaysReadAuthorization()
		# Cache for a long time
		cache = SimpleCache(timeout=24 * 60 * 60)
		filtering = {
			'name': FILTERS.TEXT,
			# Add a filter to allow looking up all tags referenced by the metadata of a specific dataset
			# see buid_filters below for implementation
			'dataset': 'exact'
		}
		ordering = ['name']
		# Disable the hard and soft limit as the number of tags will remain fairly small
		limit = None
		max_limit = None
		queryset = Tag.objects.all()
		resource_name = 'tag'
		serializer = Serializer()
		# Validate data on submission
		validation = FormValidation(form_class = modelform_factory(Tag, fields='__all__'))

	
	def build_filters(self, filters=None, ignore_bad_filters=False):
		'''Given a dictionary of filters, create the necessary ORM-level filters'''
		
		# "dataset" is not a resource field, build_filters will therefore remove it, so we need to put it back
		orm_filters = super().build_filters(filters, ignore_bad_filters=True)
		if filters and 'dataset' in filters:
			orm_filters['dataset'] = filters['dataset']
		
		return orm_filters
	
	def apply_filters(self, request, applicable_filters):
		'''Apply the filters to the object list'''
		
		# "dataset" is not a resource field, so we can't use regular filter lookup and must create an adhoc Django ORM filter
		dataset_name = applicable_filters.pop('dataset', None)
		
		if dataset_name is None:
			return super().apply_filters(request, applicable_filters)
		else:
			# If the dataset does not exist, no tag should be returned
			try:
				dataset = Dataset.objects.get(name=dataset_name)
			except Dataset.DoesNotExist:
				return super().apply_filters(request, applicable_filters).none()
			else:
				# Filter by using the related name for the many to many relation
				# See BaseMetadata model definition
				foreign_key_related_name = dataset.metadata_content_type.app_label + '_' + dataset.metadata_content_type.model
				applicable_filters[foreign_key_related_name + '__isnull'] = False
				# Avoid duplicate results by using distinct
				return super().apply_filters(request, applicable_filters).distinct()
	
	def get_via_uri(self, uri, request=None):
		'''Pull apart the salient bits of the URI and populates the resource via a obj_get'''
		# HACK: There is a BUG in tastypie which affect resource URI with spaces and special characteristics
		# the method get_resource_uri use django.urls.reverse to convert a ressource to it's URI
		# and reverse quotes the returned URI, but get_via_uri does not unquote it first
		return super().get_via_uri(unquote(uri), request)
