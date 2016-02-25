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
	
	characteristics = fields.ToManyField(CharacteristicResource, 'characteristics')
	#TODO check here
#	characteristics = fields.ListField()
	instrument = fields.CharField('instrument')
	telescope = fields.CharField('telescope')
	
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
		
	def dehydrate(self, bundle):
		#TODO check here
		# bundle.data['characteristics'] = [str(name) for name in bundle.obj.characteristics.values_list('name', flat = True)]
		return bundle



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
		for field in self.Meta.object_class._meta.get_fields():
			if not field.is_relation:
    				self._meta.filtering.setdefault(field.name, ALL)
    				self._meta.ordering.append(field.name)