from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS, url
from tastypie.authorization import DjangoAuthorization
from tastypie.utils import trailing_slash


# See http://django-tastypie.readthedocs.org/en/latest/paginator.html why it is important for postgres to have a special paginator
from common.tastypie_paginator import EstimatedCountPaginator

from dataset.models import Dataset, Characteristic



class CharacteristicResource(ModelResource):
	class Meta:
		queryset = Characteristic.objects.all()
		resource_name = 'characteristic'
		limit = None
		paginator_class = EstimatedCountPaginator
		authorization = DjangoAuthorization()

class DatasetResource(ModelResource):
	characteristics = fields.ToManyField(CharacteristicResource, 'characteristics', full = True)
	class Meta:
		queryset = Dataset.objects.all()
		resource_name = 'dataset'
		limit = None
		paginator_class = EstimatedCountPaginator
		authorization = DjangoAuthorization()
		filtering = {
		"instrument": ALL,
		"telescope": ALL,
		"characteristics": ALL_WITH_RELATIONS
		}
