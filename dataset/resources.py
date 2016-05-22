from copy import copy
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models.constants import LOOKUP_SEP

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from SDA.resources import ResourceMeta
from dataset.models import DataLocation, Dataset, Characteristic, Instrument, Telescope, Keyword

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
			uri = reverse('api_dispatch_list', kwargs={'resource_name': bundle.obj.id, 'api_name': self.api_name})
		except (NoReverseMatch, AttributeError):
			return None
		
		# get the metadata resource for the dataset
		metadata_resource = self._meta.api.canonical_resource_for(bundle.obj.id)
		
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

