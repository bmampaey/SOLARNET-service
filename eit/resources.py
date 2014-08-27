from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS, url
from tastypie.authorization import DjangoAuthorization
from tastypie.utils import trailing_slash

# See http://django-tastypie.readthedocs.org/en/latest/paginator.html why it is important for postgres to have a special paginator
from SDA.paginator import EstimatedCountPaginator
from eit.models import MetaData, Keyword, DataLocation
#from dataset.resources import DataSetResource

class DataSetResource(ModelResource):
	class Meta:
		limit = 20
		#include_absolute_url = True
		paginator_class = EstimatedCountPaginator
		authorization = DjangoAuthorization()
	
	def base_urls(self):
		"""
		The standard URLs this ``Resource`` should respond to.
		"""
		# Due to the way Django parses URLs, ``get_multiple`` won't work without
		# a trailing slash.
		return [
			url(r"^%s/(?P<resource_name>%s)%s$" % (self.data_set_name, self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
			url(r"^%s/(?P<resource_name>%s)/schema%s$" % (self.data_set_name, self._meta.resource_name, trailing_slash()), self.wrap_view('get_schema'), name="api_get_schema"),
			url(r"^%s/(?P<resource_name>%s)/set/(?P<pk_list>\w[\w/;-]*)/$" % (self.data_set_name, self._meta.resource_name), self.wrap_view('get_multiple'), name="api_get_multiple"),
			url(r"^%s/(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)%s$" % (self.data_set_name, self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
		]

class KeywordResource(DataSetResource):
	class Meta(DataSetResource.Meta):
		queryset = Keyword.objects.all()
		resource_name = 'keyword'
	
	def __init__(self, data_set_name, *args, **kwargs):
		self.data_set_name = data_set_name
		self._meta.paginator_class.setup(connection_name = data_set_name)
		super(KeywordResource, self).__init__(*args, **kwargs)

class DataLocationResource(DataSetResource):
	meta_data = fields.OneToOneField('eit.resources.MetaDataResource', 'meta_data', null=True, blank=True)
	class Meta(DataSetResource.Meta):
		queryset = DataLocation.objects.all()
		resource_name = 'data_location'
	
	def __init__(self, data_set_name, *args, **kwargs):
		self.data_set_name = data_set_name
		self._meta.paginator_class.setup(connection_name = data_set_name)
		super(DataLocationResource, self).__init__(*args, **kwargs)

class MetaDataResource(DataSetResource):
	data_location = fields.OneToOneField(DataLocationResource, 'data_location', null=True, blank=True)
	class Meta(DataSetResource.Meta):
		queryset = MetaData.objects.all()
		resource_name = 'meta_data'
	
	def __init__(self, data_set_name, *args, **kwargs):
		self.data_set_name = data_set_name
		self._meta.paginator_class.setup(connection_name = data_set_name)
		super(MetaDataResource, self).__init__(*args, **kwargs)


