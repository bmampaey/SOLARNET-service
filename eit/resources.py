from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization

# See http://django-tastypie.readthedocs.org/en/latest/paginator.html why it is important for postgres to have a special paginator
from SDA.paginator import EstimatedCountPaginator
from eit.models import MetaData

class MetaDataResource(ModelResource):
	class Meta:
		queryset = MetaData.objects.all()
		resource_name = 'eit'
		limit = 20
		paginator_class = EstimatedCountPaginator.with_setup(connection_name = "eit")
		authorization = DjangoAuthorization()
