from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

# TODO this should be done with api keys and a custom user model
class UserResource(ModelResource):
	'''Allow to login or logout a user that is not staff from email only. On login create user if it does not exists.'''
	class Meta:
		queryset = User.objects.all()
		fields = ['email']
		allowed_methods = ['get', 'post']
		resource_name = 'user'
		list_allowed_methods = []
        detail_allowed_methods = []
	
	def prepend_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash), self.wrap_view('login'), name="api_login"),
			url(r'^(?P<resource_name>%s)/logout%s$' % (self._meta.resource_name, trailing_slash), self.wrap_view('logout'), name='api_logout'),
		]
	
	def login(self, request, **kwargs):
		self.method_check(request, allowed=['post'])
		
		# Extract the email from the request data
		data = self.deserialize(request, request.body)
		email = data.get('email', '')
		
		# We extract the user/password from it's email
		username, password = email.split('@', 1)
		
		user = authenticate(username=username, password=password)
		
		if user is None:
			# User does not exists, register the user
			try:
				User.objects.create_user(username, email=email, password=password)
			except IntegrityError, why:
				pass
			else:
				user = authenticate(username=username, password=password)
		
		if user:
			if user.is_staff:
				return self.create_response(request, {'success': False, 'reason': 'Staff users cannot log using only email. Please log through the administration interface.'}, HttpForbidden)
			elif not user.is_active:
				return self.create_response(request, {'success': False, 'reason': 'Your account is disabled. Please contact the site administrators for help.'}, HttpForbidden)
			else:
				login(request, user)
				return self.create_response(request, {'success': True, 'username': user.username})
		else:
			return self.create_response(request, {'success': False, 'reason': 'Please check that you are using the same email as previously.'}, HttpUnauthorized)
	
	def logout(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		if request.user and request.user.is_authenticated():
			logout(request)
			return self.create_response(request, {'success': True})
		else:
			return self.create_response(request, {'success': False}, HttpUnauthorized)