from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource

from SDA.resources import ResourceMeta
from account.models import UserProfile

# TODO check the pouet, make so that profile is integrated to user

class UserResource(BaseResource):
	pouet = fields.OneToOneField('account.resources.UserProfileResource', 'UserProfile', null=True)
	fixed = fields.CharField(default=reverse('api_dispatch_list', kwargs = {'resource_name' : 'user_profile', 'api_name':'v1'}), readonly=True, help_text="URL of the meta-data resource")
	
	class Meta(ResourceMeta):
		queryset = User.objects.all()

class UserProfileResource(BaseResource):
	user=fields.OneToOneField(UserResource, 'user')
	
	class Meta(ResourceMeta):
		queryset = UserProfil.objects.all()
