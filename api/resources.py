from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.urls import re_path
from django.db import IntegrityError

from tastypie.resources import Resource
from tastypie.http import HttpBadRequest, HttpCreated, HttpNoContent
from tastypie.authentication import BasicAuthentication

from .serializers import Serializer

__all__ = ['UserResource']

# The user ressource behavior is modified from the usual ressources behavior,
# so that it only acts on the list endpoint (/user) and no other endpoints (e.g. detail)
# and only act on the user that made the request, authentified by it's email and password

# TODO override User model to add api_key and add a property name as the fill name (and change test also)

class UserResource(Resource):
	'''RESTful resource for model User to allow to create/read/update/delete users'''
	
	class Meta:
		# Allow only methods corresponding to create/read/update/delete
		allowed_methods = ['post', 'get', 'patch', 'delete']
		authentication = BasicAuthentication()
		# authorization is irrelevant because the user can only act on it's own profile
		serializer = Serializer()
		resource_name = 'user'
	
	def base_urls(self):
		'''The standard URLs this Resource should respond to'''
		# Override the URLs so that only the list URLs are presented
		return [
			re_path(r'^(?P<resource_name>%s)/$' % self._meta.resource_name, self.wrap_view('dispatch_list'), name='api_dispatch_list'),
			re_path(r'^(?P<resource_name>%s)/schema/$' % self._meta.resource_name, self.wrap_view('get_schema'), name='api_get_schema'),
		]
	
	def is_authenticated(self, request):
		'''Handles checking if the user is authenticated and dealing with unauthenticated users'''
		# Bypass authentication for POST so that new users can create an account
		if request.method.lower() != 'post':
			super().is_authenticated(request)
	
	def post_list(self, request, **kwargs):
		'''Create a new user and returns it's full name and api_key'''
		
		# Extract the email, username and password from the request data
		data = self.deserialize(request, request.body)
		email = data.get('email', '')
		password = data.get('password', '')
		first_name = data.get('first_name', '')
		last_name = data.get('last_name', '')
		
		# Check that the provided email is valid
		try:
			EmailValidator()(email)
		except ValidationError as error:
			return self.error_response(request, {'error': error.message}, response_class=HttpBadRequest)
		
		# Create the user using it's email as username
		# If a user with the same username already exists, it will raise an IntegrityError
		try:
			user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
		except IntegrityError:
			 return self.error_response(request, {'error': 'An account with this email already exists.'}, response_class=HttpBadRequest)
		else:
			return self.create_response(request,  {'name': user.get_full_name(), 'api_key': user.api_key.key}, response_class=HttpCreated)
	
	def get_list(self, request, **kwargs):
		'''Authenticate a user and return it's username and api_key'''
		# Authentication is done by the dispatch method
		return self.create_response(request, {'name': request.user.get_full_name(), 'api_key': request.user.api_key.key})
	
	def patch_list(self, request, **kwargs):
		'''Authenticate a user and update it's password and api_key and return them'''
		# Authentication is done by the dispatch method
		
		# Extract the new password from the request data
		data = self.deserialize(request, request.body)
		password = data.get('password', '')
		
		# Change the password and the api key
		request.user.set_password(password)
		request.user.save()
		request.user.api_key.key = None
		request.user.api_key.save()
		return self.create_response(request, {'name': request.user.get_full_name(), 'api_key': request.user.api_key.key})
	
	def delete_list(self, request, **kwargs):
		'''Authenticate a user and delete it'''
		# Authentication is done by the dispatch method
		request.user.delete()
		return HttpNoContent()
	
	def get_schema(self, request, **kwargs):
		'''Returns a serialized form of the schema of the resource'''
		data = {
			'default_format': self._meta.default_format,
			'allowed_list_http_methods': self._meta.list_allowed_methods,
		}
		return self.create_response(request, data)
