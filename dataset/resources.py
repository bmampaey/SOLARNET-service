from copy import copy
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models.constants import LOOKUP_SEP

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from SDA.resources import ResourceMeta
from dataset.models import DataLocation, Tag, Dataset, Characteristic, Instrument, Telescope, Keyword

class TagResource(ModelResource):
	'''RESTful resource for model Tag'''
	# TODO check how to add metadata in detail view ListField?
	# Better add the related fields at run time
	
	class Meta(ResourceMeta):
		queryset = Tag.objects.all()
		resource_name = 'tag'
		filtering = {'name': ALL}


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
	characteristics = fields.ListField()
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
		
		
	def dehydrate_characteristics(self, bundle):
		return [str(name) for name in bundle.obj.characteristics.values_list('name', flat = True)]

	def dehydrate_metadata2(self, bundle):
		# 2 ways
		# 1.  use the request and the resource to build everything
		# 2. use the reverse and the buil_filters
		from SDA.api import api
		# Get the API resource for the metadata
		try:
			#import pdb; pdb.set_trace()
			resource = api._registry['%s_metadata' % bundle.obj.id]
		except KeyError:
			return None
		
		request = copy(bundle.request)
		# TODO remove dataset only filters from GET QueryDict
		request.path = resource.get_resource_uri()
		number_items = resource.obj_get_list(resource.build_bundle(request=request)).count()
		return {'uri': request.get_full_path(), 'number_items': number_items}

	def dehydrate_metadata(self, bundle):
		#import pdb; pdb.set_trace()
		# Find the metadata resource uri
		try:
			uri = reverse('api_dispatch_list', kwargs={'resource_name': '%s_metadata' % bundle.obj.id, 'api_name': self.api_name})
		except NoReverseMatch:
			return None
		
		# Create the resource for the metadata model
		class MetadataResource(BaseMetadataResource):
				class Meta(BaseMetadataResource.Meta):
					queryset = bundle.obj.metadata_model.objects.all()
		
		# Get the filters from the GET query string
		query_dict = bundle.request.GET.copy()
		
		# Ignore bad filters because a filter can be correct for one dataset but not the orther
		filters = MetadataResource().build_filters(query_dict, ignore_bad_filters=True)
		
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
				 'number_items': bundle.obj.metadata_model.objects.filter(**filters).count()
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