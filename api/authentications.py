from django.contrib.auth.models import User, AnonymousUser
from django.db.models import signals
from tastypie.authentication import ApiKeyAuthentication
from tastypie.models import create_api_key
from tastypie.http import HttpUnauthorized

__all__ = ['ApiKeyOrAnonymousAuthentication']

class ApiKeyOrAnonymousAuthentication(ApiKeyAuthentication):
	'''Authentication for User account using the username and API key but default to AnonymousUser if the credentials couls not be verified'''
	
	def is_authenticated(self, request, **kwargs):
		'''Finds the user and checks their API key'''
		
		res = super().is_authenticated(request, **kwargs)
		
		# In case of authentication error, we receive an HttpUnauthorized, else we received True
		if isinstance(res, HttpUnauthorized):
			
			request.user = AnonymousUser()
			res = True
		
		return res


# Register signal to add api key on django auth user creation
signals.post_save.connect(create_api_key, sender=User)
