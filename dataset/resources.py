from copy import copy
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models.constants import LOOKUP_SEP
from django.db.models import Q

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.exceptions import InvalidFilterError

from SDA.resources import ResourceMeta
from dataset.models import DataLocation, Tag, Dataset, Characteristic, Instrument, Telescope, Keyword

from .filters import ComplexFilter, ParseException

class TagResource(ModelResource):
	'''RESTful resource for model Tag'''
	# TODO check how to add metadata in detail view ListField?
	# Better add the related fields at run time
	
	class Meta(ResourceMeta):
		queryset = Tag.objects.all()
		resource_name = 'tag'
		filtering = {'name': ALL}
	
	def build_filters(self, filters=None, ignore_bad_filters=False):
		# Allow more intuitive  tags filtering on dataset using dataset={dateset_id} instaed of {dataset_id}_metadata__isnull=False
		# This filter allows only to get tags for one dataset
		orm_filters = super(TagResource, self).build_filters(filters, ignore_bad_filters)
		if "dataset" in filters:
			orm_filters[filters['dataset'] + '_metadata__isnull'] = False
		
		return orm_filters
	
	def apply_filters(self, request, applicable_filters):
		# Avoid duplicate results
		return super(TagResource, self).apply_filters(request, applicable_filters).distinct()
	
	def build_schema(self):
		data = super(TagResource, self).build_schema()
		data['filtering']['dataset'] = 'exact'
		return data

class DataLocationResource(ModelResource):
	'''Resource for DataLocation models'''
	# TODO check how to add metadata in detail view ListField?
	# Better add the related fields at run time
	class Meta(ResourceMeta):
		queryset = DataLocation.objects.all()
		resource_name = 'data_location'

class TelescopeResource(ModelResource):
	'''RESTful resource for model Telescope'''
	instruments = fields.ToManyField('dataset.resources.InstrumentResource', 'instruments', full = True)
	
	class Meta(ResourceMeta):
		queryset = Telescope.objects.all()
		resource_name = 'telescope'
		allowed_methods = ['get']
		max_limit = None
		limit = None
		filtering = {
			"name": ALL,
			"description": ALL,
		}


class InstrumentResource(ModelResource):
	'''RESTful resource for model Instrument'''
	
	telescope = fields.ToOneField(TelescopeResource, 'telescope')
	
	class Meta(ResourceMeta):
		queryset = Instrument.objects.all()
		resource_name = 'instrument'
		allowed_methods = ['get']
		max_limit = None
		limit = None
		filtering = {
			"name": ALL,
			"description": ALL,
		}


class CharacteristicResource(ModelResource):
	'''RESTful resource for model Characteristic'''
	
	datasets = fields.ToManyField('dataset.resources.DatasetResource', 'datasets')
	
	class Meta(ResourceMeta):
		queryset = Characteristic.objects.all()
		resource_name = 'characteristic'
		allowed_methods = ['get']
		max_limit = None
		limit = None
		filtering = {
			"name": ALL,
		}


class KeywordResource(ModelResource):
	'''RESTful resource for model Keyword'''
	
	dataset = fields.ToOneField('dataset.resources.DatasetResource', 'dataset')
	
	class Meta(ResourceMeta):
		queryset = Keyword.objects.all()
		resource_name = 'keyword'
		allowed_methods = ['get']
		filtering = {
			'dataset': ALL_WITH_RELATIONS,
			'db_column': ALL,
			'name': ALL,
			'python_type': ALL,
			'unit': ALL,
			'description': ALL,
		}


class DatasetResource(ModelResource):
	'''RESTful resource for model Dataset'''
	
	instrument = fields.CharField('instrument')
	telescope = fields.CharField('telescope')
	characteristics = fields.ToManyField(CharacteristicResource, 'characteristics', full=True)

	metadata = fields.DictField()
	
	class Meta(ResourceMeta):
		queryset = Dataset.objects.all()
		resource_name = 'dataset'
		allowed_methods = ['get']
		max_limit = None
		limit = None
		filtering = {
			"name": ALL,
			"description": ALL,
			"contact": ALL,
			"instrument": ALL,
			"telescope": ALL,
			"characteristics": ALL_WITH_RELATIONS
		}
	
	def dehydrate_metadata(self, bundle):
		# Find the metadata resource uri
		try:
			uri = reverse('api_dispatch_list', kwargs={'resource_name': '%s_metadata' % bundle.obj.id, 'api_name': self.api_name})
		except (NoReverseMatch, AttributeError):
			return None
		
		# get the metadata resource for the dataset
		metadata_resource = self._meta.api.canonical_resource_for(bundle.obj.id + '_metadata')
		
		# Get the filters from the GET query string
		query_dict = bundle.request.GET.copy()
		
		# Ignore bad filters because a filter can be correct for one dataset but not the orther
		filters = metadata_resource.build_filters(query_dict, ignore_bad_filters=True)
		
		# Remove from query_dict any filter that was ignored
		for item in query_dict.keys():
			try:
				field_name, trash = item.split(LOOKUP_SEP, 1)
			except ValueError:
				field_name = item
			if not any(filter.startswith(field_name) for filter in filters):
				query_dict.pop(item)
		
		# Add the query string to the metadata resource uri
		if query_dict:
			uri = uri + '?' + query_dict.urlencode()
		
		return {
			'uri': uri,
			'number_items': metadata_resource.apply_filters(bundle.request, filters).count()
		}


class BaseMetadataResource(ModelResource):
	'''Base resource for Metadata models'''
	
	data_location = fields.ToOneField(DataLocationResource, 'data_location', full=True)
	tags = fields.ToManyField(TagResource, 'tags', full=True)
	
	class Meta(ResourceMeta):
		excludes = ['id']
		detail_uri_name = 'oid'
		filtering = {'tags': ALL_WITH_RELATIONS}
		ordering = []
	
	def __init__(self):
		super(BaseMetadataResource, self).__init__()
		# Add filtering and ordering by all regular fields
		if getattr(self._meta, 'object_class', None) is not None:
			for field in self._meta.object_class._meta.get_fields():
				if not field.is_relation and not field.auto_created:
	    				self._meta.filtering.setdefault(field.name, ALL)
	    				self._meta.ordering.append(field.name)
	
	def build_filters(self, filters=None, ignore_bad_filters=False):
		'''Allow more complex filtering on metadata using search parameter'''
		#import pdb; pdb.set_trace()
		search_filters = filters.getlist('search', None)
		orm_filters = super(BaseMetadataResource, self).build_filters(filters, ignore_bad_filters)
		
		if search_filters is not None:
			try:
				orm_filters['search'] = reduce(lambda a, b: a & ComplexFilter.parseString(b)[0].as_q(), search_filters, Q())
			except ParseException, why:
				if not ignore_bad_filters:
					raise InvalidFilterError(str(why))
		
		return orm_filters
	
	def apply_filters(self, request, applicable_filters):
		'''Apply complex search filter'''
		#import pdb; pdb.set_trace()
		search_filter = applicable_filters.pop('search', None)
		partially_filtered = super(BaseMetadataResource, self).apply_filters(request, applicable_filters)
		if search_filter is not None:
			applicable_filters['search'] = search_filter
			return partially_filtered.filter(search_filter)
		else:
			return partially_filtered
