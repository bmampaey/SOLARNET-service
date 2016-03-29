from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


from wizard.models import UserDataSelection, DataSelection
from common.models import BaseTag
from SDA.authorization import AlwaysReadAuthorization

class UserDataSelectionResource(ModelResource):
	data_selections = fields.ToManyField('wizard.resources.DataSelectionResource', 'data_selections', related_name='name', full = True)
	number_items = fields.IntegerField(attribute='number_items', readonly = True)
	class Meta:
		queryset = UserDataSelection.objects.all()
		resource_name = 'user_data_selection'
		limit = None
		authorization = AlwaysReadAuthorization()
		filtering = {
		"user": ALL,
		"name": ALL,
		"created": ALL,
		"updated": ALL,
		}

class DataSelectionResource(ModelResource):
	user_data_selection = fields.ForeignKey(UserDataSelectionResource, 'user_data_selection', full = False)
	dataset = fields.CharField(attribute='dataset')
	
	class Meta:
		queryset = DataSelection.objects.all()
		resource_name = 'data_selection'
		limit = None
		authorization = AlwaysReadAuthorization()
		filtering = {
		"dataset": ALL_WITH_RELATIONS,
		"created": ALL,
		}
