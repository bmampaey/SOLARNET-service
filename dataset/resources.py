from tastypie import fields
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS, url
from tastypie.authorization import DjangoAuthorization
from tastypie.utils import trailing_slash


# See http://django-tastypie.readthedocs.org/en/latest/paginator.html why it is important for postgres to have a special paginator
from common.tastypie_paginator import EstimatedCountPaginator

from dataset.models import Dataset, Characteristic, Instrument, Telescope

class TelescopeResource(ModelResource):
	instruments = fields.ToManyField('dataset.resources.InstrumentResource', 'instruments', related_name='name', full = True)
	
	class Meta:
		queryset = Telescope.objects.all()
		resource_name = 'telescope'
		allowed_methods = ['get']
		limit = None
		authorization = DjangoAuthorization()
		filtering = {
		"name": ALL,
		"description": ALL,
		}

class InstrumentResource(ModelResource):
	telescope = fields.ForeignKey(TelescopeResource, 'telescope', full = False)
	
	class Meta:
		queryset = Instrument.objects.all()
		resource_name = 'instrument'
		allowed_methods = ['get']
		limit = None
		authorization = DjangoAuthorization()
		filtering = {
		"name": ALL,
		"description": ALL,
		}

class CharacteristicResource(ModelResource):
	class Meta:
		queryset = Characteristic.objects.all()
		resource_name = 'characteristic'
		limit = None
		paginator_class = EstimatedCountPaginator
		authorization = DjangoAuthorization()

class TagResource(Resource):
	
	name = fields.CharField(attribute = 'name')
	
	class Meta:
		allowed_methods = ['get']
		include_resource_uri = False
		resource_name = 'tag'
		limit = None
		authorization = DjangoAuthorization()
	
	class Tag:
		def __init__(self, **kwargs):
			for key, val in kwargs.iteritems():
				setattr(self, key, val)
	
	def obj_get_list(self, request = None, **kwargs):
		# outer get of object list... this calls get_object_list and
		# could be a point at which additional filtering may be applied
		return [self.Tag(name=name) for name in BaseTag.all_tags()]
	
#	def obj_get(self, request = None, **kwargs):
#		# get one object from data source
#		pk = int(kwargs['pk'])
#		try:
#			return data[pk]
#		except KeyError:
#			raise NotFound("Object not found") 

class DatasetResource(ModelResource):
	characteristics = fields.ToManyField(CharacteristicResource, 'characteristics', full = False)
	#TODO check here
#	characteristics = fields.ListField()
	instrument = fields.CharField('instrument')
	telescope = fields.CharField('telescope')
	
	class Meta:
		queryset = Dataset.objects.all()
		resource_name = 'dataset'
		limit = None
		paginator_class = EstimatedCountPaginator
		authorization = DjangoAuthorization()
		filtering = {
		"name": ALL,
		"description": ALL,
		"contact": ALL,
		"instrument": ALL,
		"telescope": ALL,
		"characteristics": ALL_WITH_RELATIONS
		}
		
	def dehydrate(self, bundle):
		bundle.data['characteristics'] = [str(name) for name in bundle.obj.characteristics.values_list('name', flat = True)]
		return bundle
