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

class DatasetResource(ModelResource):
#	characteristics = fields.ToManyField(CharacteristicResource, 'characteristics', full = False)
	characteristics = fields.ListField()
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