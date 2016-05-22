from django.http import QueryDict
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from SDA.resources import ResourceMeta
from SDA.authorizations import UserOnlyModifAuthorization
from web_account.authentication import WebUserApiKeyAuthentication
from data_selection.models import DataSelectionGroup, DataSelection

from dataset.resources import DatasetResource

class DataSelectionGroupResource(ModelResource):
	'''RESTful resource for model DataSelectionGroup'''
	
	data_selections = fields.ToManyField('data_selection.resources.DataSelectionResource', 'data_selections', full = True, null = True, blank = True)
	number_items = fields.IntegerField(attribute = 'number_items', readonly = True, help_text = 'The cumulated number of metadata items in the data selections')
	ftp_link = fields.CharField(attribute='ftp_link', readonly = True, help_text = "A FTP link to the data selection")
	
	class Meta(ResourceMeta):
		queryset = DataSelectionGroup.objects.all()
		resource_name = 'data_selection_group'
		authentication = WebUserApiKeyAuthentication()
		authorization = UserOnlyModifAuthorization('user')
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'name': ALL,
			'created' : ALL,
			'updated' : ALL,
		}
	
	def obj_create(self, bundle, **kwargs):
		# make sure that a new user data selection belongs to the autenthicated user
		return super(DataSelectionGroupResource, self).obj_create(bundle, user=bundle.request.user)
	
	def authorized_read_list(self, object_list, bundle):
		# Only allow a user to list it's own data selection
		if bundle.request.user.is_authenticated():
			return object_list.filter(user=bundle.request.user)
		else:
			return object_list.none()

class DataSelectionResource(ModelResource):
	'''RESTful resource for model DataSelection'''
	
	data_selection_group = fields.ToOneField(DataSelectionGroupResource, 'data_selection_group')
	dataset = fields.ToOneField(DatasetResource, 'dataset', full = True)
	
	class Meta(ResourceMeta):
		queryset = DataSelection.objects.all()
		resource_name = 'data_selection'
		authentication = WebUserApiKeyAuthentication()
		authorization = UserOnlyModifAuthorization('data_selection_group__user')
		excludes = ['query']
		filtering = {
			'data_selection_group' : ALL_WITH_RELATIONS,
			'dataset' : ALL_WITH_RELATIONS,
			'query_string' : ALL,
			'created' : ALL,
			'number_items' : ALL,
		}
	
	def obj_create(self, bundle, **kwargs):
		# fully hydrate the bundle so the dataset get hydrated
		bundle = self.full_hydrate(bundle)
		
		# get the metadata resource for the dataset
		metadata_resource = self._meta.api.canonical_resource_for(bundle.obj.dataset.id)
		
		# create the QueryDict from the query string
		query_dict = QueryDict(bundle.obj.query_string, mutable=True)
		
		# create the filters from the ressource
		filters = metadata_resource.build_filters(query_dict, ignore_bad_filters=True)
		
		# create the QuerySet from the filters
		query_set = metadata_resource.apply_filters(bundle.request, filters)
		
		# add the query to the object
		return super(DataSelectionResource, self).obj_create(bundle, query=query_set.query)