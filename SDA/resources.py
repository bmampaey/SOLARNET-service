from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields

from SDA.models import UserProfile

class UserResource(ModelResource):
	pouet = fields.OneToOneField('SDA.resources.UserProfileResource', 'UserProfil', null=True)
	fixed = fields.CharField(default=reverse('api_dispatch_list', kwargs = {'resource_name' : 'user_profile', 'api_name':'v1'}), readonly=True, help_text="URL of the meta-data resource")
	class Meta:
		limit = 20
		queryset = User.objects.all()
#		include_absolute_url = True
		resource_name = 'user'

class UserProfileResource(ModelResource):
	user=fields.OneToOneField(UserResource, 'user')
	
	class Meta:
		limit = 20
		queryset = UserProfil.objects.all()
		resource_name = 'user_profile'
