from common.resources import BaseDataSetResource
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS, url
from tastypie.authorization import DjangoAuthorization
from tastypie.utils import trailing_slash
from swap.models import Keyword, DataLocation, MetaData

data_set_name = 'swap'

class KeywordResource(BaseDataSetResource):
	
	class Meta(BaseDataSetResource.Meta):
		queryset = Keyword.objects.all()
		resource_name = data_set_name + '_keyword'
		resource_type = 'keyword'

	def __init__(self, *args, **kwargs):
		self.data_set_name = data_set_name
		self._meta.paginator_class.setup(connection_name = self.data_set_name)
		super(KeywordResource, self).__init__(*args, **kwargs)

class DataLocationResource(BaseDataSetResource):
	meta_data = fields.OneToOneField(data_set_name+'.resources.MetaDataResource', 'meta_data', related_name='data_location', null=True, blank=True)

	class Meta(BaseDataSetResource.Meta):
		queryset = DataLocation.objects.all()
		resource_name = data_set_name + '_data_location'
		resource_type = 'data_location'

	def __init__(self, *args, **kwargs):
		self.data_set_name = data_set_name
		self._meta.paginator_class.setup(connection_name = self.data_set_name)
		super(DataLocationResource, self).__init__(*args, **kwargs)


class MetaDataResource(BaseDataSetResource):
	data_location = fields.OneToOneField(data_set_name+'.resources.DataLocationResource', 'data_location', related_name='meta_data', null=True, blank=True)

	class Meta(BaseDataSetResource.Meta):
		queryset = MetaData.objects.all()
		resource_name = data_set_name + '_meta_data'
		resource_type = 'meta_data'

	def __init__(self, *args, **kwargs):
		self.data_set_name = data_set_name
		self._meta.paginator_class.setup(connection_name = self.data_set_name)
		super(MetaDataResource, self).__init__(*args, **kwargs)

