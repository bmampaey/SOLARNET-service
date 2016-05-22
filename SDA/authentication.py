from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.db.models import signals
from tastypie.authentication import ApiKeyAuthentication
from tastypie.models import create_api_key
from tastypie.http import HttpUnauthorized

class AuthUserApiKeyAuthentication(ApiKeyAuthentication):
	''' Similar to Tastypie ApiKeyAuthentication but accept AnonymousUser '''
	
	def is_authenticated(self, request, **kwargs):
		
		res = super(AuthUserApiKeyAuthentication, self).is_authenticated(request, **kwargs)
		
		# in case of error, we receive an HttpUnauthorized
		if isinstance(res, HttpUnauthorized):
			
			request.user = AnonymousUser()
			res= True
		
		return res


# Register signal to add api key on auth user creation
signals.post_save.connect(create_api_key, sender=User)