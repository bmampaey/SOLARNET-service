from django.contrib.auth.models import User
from tastypie.resources import ModelResource

from SDA.resources import ResourceMeta

class UserResource(ModelResource):
	
	class Meta(ResourceMeta):
		queryset = User.objects.all()
		allowed_methods = ['post']
		fields = ['username']

