from urllib.parse import unquote
from django.core.exceptions import FieldError
from django.forms import modelform_factory
from tastypie.validation import FormValidation
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.paginator import Paginator
from tastypie.exceptions import InvalidFilterError

from api.authentications import ApiKeyOrAnonymousAuthentication
from api.authorizations import AlwaysReadAuthorization
from api.serializers import Serializer
from api.constants import FILTERS, FIELD_FILTERS
from api.complex_filters import get_complex_filter
from dataset.resources import DataLocationResource
from .tag import TagResource

__all__ = ['BaseMetadataResource']


class MetadataPaginator(Paginator):
	'''Paginator for the Metadata resources that substitute the count (i.e. the number of items in the list) fo an estimated count'''
	
	def get_count(self):
		'''Return the estimated count'''
		return self.objects.estimated_count()


class BaseMetadataResource(ModelResource):
	'''Abstract base RESTful resource for the Metadata models'''
	
	data_location = fields.ToOneField(DataLocationResource, 'data_location', full=True, null=True)
	tags = fields.ToManyField(TagResource, 'tags', full=True, blank=True)
	
	class Meta:
		abstract = True
		# Allow only methods corresponding to create/read on the list URL and read/update/delete on the detail URL
		list_allowed_methods = ['post', 'get']
		detail_allowed_methods = ['get', 'patch', 'delete']
		# When requesting to create/update 1 or more objects, return the objects in the response
		always_return_data = True
		authentication = ApiKeyOrAnonymousAuthentication()
		authorization = AlwaysReadAuthorization()
		# Force lookup by oid and not by pk or id (do not set a cache, or it will break the delete and upate)
		detail_uri_name = 'oid'
		excludes = ['id']
		filtering = {
			'tags': FILTERS.RELATIONAL,
			# Allow metadata filtering using a complex search expression
			# see buid_filters below for implementation
			'search': FILTERS.COMPLEX_SEARCH_EXPRESSION
		}
		max_limit = 100
		paginator_class = MetadataPaginator
		serializer = Serializer()
		# Needed so that in __init__ we know if validation was overriden in a subclass
		validation = None
	
	def __init__(self):
		super().__init__()
		
		# Add filtering and ordering for all regular fields
		# Copy them before modifying to avoid affecting other metadata ressources definitions
		self._meta.ordering = set(self._meta.ordering)
		self._meta.filtering = dict(self._meta.filtering)
		
		for field in self._meta.object_class._meta.get_fields():
			if not field.is_relation and not field.auto_created:
				try:
					filter = FIELD_FILTERS[type(field)]
				except KeyError:
					pass
				else:
					self._meta.ordering.add(field.name)
					self._meta.filtering[field.name] = filter
		
		# Add default form validation here, because this is an abstract ressource so the object_class is only known when subclassed
		if self._meta.validation is None:
			self._meta.validation = FormValidation(form_class = modelform_factory(self._meta.object_class, fields='__all__'))
	
	# By default, ignore bad filters such that:
	# - if filtering is done accross datasets, and some filters are not pertinant for this metadata, they will be ignored
	# - if the filters in the query_string of a data selection are not pertinant for this metadata, they will be ignored
	def build_filters(self, filters=None, ignore_bad_filters=True):
		'''Given a dictionary of filters, create the necessary ORM-level filters'''
		
		# Some keys have a special meaning, so must be excluded from the filters
		# If one must filter on one of these keywords, then use the __exact suffix, for example offset__exact = 0
		# Copy the filters as to not modify the function input
		filters = filters.copy()
		
		special_keys = {}
		for special_key in ('offset', 'limit', 'search'):
			special_keys[special_key] = filters.pop(special_key, [])
		
		filters = super().build_filters(filters, ignore_bad_filters)
		
		# Convert the complex search expressions into filters usable by Django ORM
		if special_keys['search']:
			filters['search'] = [get_complex_filter(search_expression, ignore_bad_filters) for search_expression in special_keys['search']]
		
		return filters
	
	def apply_filters(self, request, applicable_filters):
		'''Apply the filters to the object list'''
		
		# Remove temporarly the "search" filters to do the default filtering
		# because it is a Q filter instead of being a regular field filter
		search_filter = applicable_filters.pop('search', None)
		
		object_list = super().apply_filters(request, applicable_filters)
		
		# Apply the "search" filter and put it back in the applicable_filters for consistency
		if search_filter:
			try:
				object_list = object_list.filter(*search_filter)
			except FieldError as why:
				raise InvalidFilterError(str(why))
			applicable_filters['search'] = search_filter
		
		# If one of the filters is tags__in, then avoid duplicate results by using distinct
		if 'tags__in' in applicable_filters:
			object_list = object_list.distinct()
		
		return object_list
	
	def is_valid(self, bundle):
		'''Checks if the data provided by the user is valid'''
		
		valid = super().is_valid(bundle)
		
		# If the metadata object is being updated (i.e. it has a pk), then the oid cannot be modified
		if bundle.obj.pk is not None:
			# We cannot use the bundle.data because it has been modified too much by tastypie :-///
			# so look into the original data sent in the request
			data = self.deserialize(bundle.request, bundle.request.body)
			
			if 'oid' in data:
				valid = False
				
				# Add an error in the bundle errors for the oid field
				if self._meta.resource_name not in bundle.errors:
					bundle.errors[self._meta.resource_name] = dict()
				if 'oid' not in bundle.errors[self._meta.resource_name]:
					bundle.errors[self._meta.resource_name]['oid'] = list()
				bundle.errors[self._meta.resource_name]['oid'].append('The value cannot be modified once it has been set')
		
		return valid
	
	def get_via_uri(self, uri, request=None):
		'''Pull apart the salient bits of the URI and populates the resource via a obj_get'''
		# HACK: There is a BUG in tastypie which affect resource URI with spaces and special characteristics
		# the method get_resource_uri use django.urls.reverse to convert a ressource to it's URI
		# and reverse quotes the returned URI, but get_via_uri does not unquote it first
		return super().get_via_uri(unquote(uri), request)
