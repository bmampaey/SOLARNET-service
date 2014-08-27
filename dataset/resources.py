from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS, url
from tastypie.authorization import DjangoAuthorization
from tastypie.utils import trailing_slash


# See http://django-tastypie.readthedocs.org/en/latest/paginator.html why it is important for postgres to have a special paginator
from SDA.paginator import EstimatedCountPaginator
from dataset.models import DataSet

class DataSetResource(ModelResource):
	class Meta:
		queryset = DataSet.objects.all()
		resource_name = 'data_set'
		limit = None
		paginator_class = EstimatedCountPaginator
		authorization = DjangoAuthorization()
