import urlparse

from django.conf import settings

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from SDA.resources import ResourceMeta
from data_selection.models import UserDataSelection, DataSelection

from dataset.resources import DatasetResource

class UserDataSelectionResource(ModelResource):
	'''RESTful resource for model UserDataSelection'''
	
	data_selections = fields.ToManyField('data_selection.resources.DataSelectionResource', 'data_selections', full = True)
	number_items = fields.IntegerField(attribute = 'number_items', readonly = True, help_text = 'The cumulated number of metadata items in the data selections')
	ftp_link = fields.CharField(readonly = True, help_text = "A FTP link to the data selection")
	
	class Meta(ResourceMeta):
		queryset = UserDataSelection.objects.all()
		resource_name = 'user_data_selection'
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'name': ALL,
			'created' : ALL,
			'updated' : ALL,
		}
	
	def dehydrate_ftp_link(self, bundle):
		return urlparse.urljoin(settings.FTP_URL, 'data_selections/{obj.user.username}/{obj.name}/'.format(obj = bundle.obj))
	
	def obj_create(self, bundle, **kwargs):
		import pdb; pdb.set_trace()
		#TODO is this needed
		return super(UserDataSelectionResource, self).obj_create(bundle, user=bundle.request.user)
	
	def authorized_read_list(self, object_list, bundle):
		# Only allow a user to list it's own data seletcion
		if bundle.request.user.is_authenticated():
			return object_list.filter(user=bundle.request.user)
		else:
			return object_list.none()

class DataSelectionResource(ModelResource):
	'''RESTful resource for model DataSelection'''
	
	user_data_selection = fields.ToOneField(UserDataSelectionResource, 'user_data_selection')
	dataset = fields.ToOneField(DatasetResource, 'dataset', full = True)
	ftp_link = fields.CharField(readonly = True, help_text = "A FTP link to the data selection")
	
	class Meta(ResourceMeta):
		queryset = DataSelection.objects.all()
		resource_name = 'data_selection'
		filtering = {
			'user_data_selection' : ALL_WITH_RELATIONS,
			'dataset' : ALL_WITH_RELATIONS,
			'query_string' : ALL,
			'metadata_oids' : ALL,
			'created' : ALL,
			'number_items' : ALL,
		}
	
	def dehydrate_ftp_link(self, bundle):
		return urlparse.urljoin(settings.FTP_URL, 'data_selections/{obj.user_data_selection.user.username}/{obj.user_data_selection.name}/{obj.dataset.name}/'.format(obj = bundle.obj))