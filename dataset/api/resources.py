from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization

# See http://django-tastypie.readthedocs.org/en/latest/paginator.html why it is important for postgres to have a special paginator
from paginator import EstimatedCountPaginator
from dataset.models import DataSet

class DataSetResource(ModelResource):
	class Meta:
		queryset = DataSet.objects.all()
		resource_name = 'dataset'
		limit = None
		include_absolute_url = False
		paginator_class = EstimatedCountPaginator
		authorization = DjangoAuthorization()
