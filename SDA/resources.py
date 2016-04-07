from SDA.authorizations import AlwaysReadAuthorization
from tastypie.authentication import ApiKeyAuthentication
from django.contrib.auth.models import AnonymousUser, User

#class AnonymousGETAuthentication(SessionAuthentication):
#	''' No authentication on GET '''
#	
#	def is_authenticated(self, request, **kwargs):
#		''' If GET, don't check authentication, otherwise fall back to parent '''
#		if request.method == "GET":
#			return True
#		else:
#			return super(AnonymousGETAuthentication, self).is_authenticated(request, **kwargs)

class MyApiKeyAuthentication(ApiKeyAuthentication):
	''' Similar to Tastypie ApiKeyAuthentication but with web account user model '''
	auth_type = 'apikey'
	
	def anonymous(self, request):
		request.user = AnonymousUser()
		return True
	
	def is_authenticated(self, request, **kwargs):
		import pdb; pdb.set_trace()
		try:
			username, api_key = self.extract_credentials(request)
		except ValueError:
			return self.anonymous(request)
		
		if not username or not api_key:
			return self.anonymous(request)
		
		try:
			user = User.objects.get(username = username)
		except (User.DoesNotExist, User.MultipleObjectsReturned):
			return self.anonymous(request)
		
		if self.check_api_key(user, api_key):
			request.user = user
			return True
		else:
			return False

	def get_key(self, user, api_key):
		"""
		Attempts to find the API key for the user. Uses ``ApiKey`` by default
		but can be overridden.
		"""
		from tastypie.models import ApiKey
		
		try:
			if user.api_key.key != api_key:
				return False
		except ApiKey.DoesNotExist:
			return False
		
		return True

	def get_identifier(self, request):
		"""
		Provides a unique string identifier for the requestor.
		This implementation returns the user's username.
		"""
		try:
			username = self.extract_credentials(request)[0]
		except ValueError:
			username = 'anonymous'
		return username


class ResourceMeta:
	"""Base class to set common parameters to all resources"""
	max_limit = 100
	authentication = MyApiKeyAuthentication()
	authorization = AlwaysReadAuthorization()
	always_return_data = True
	default_format = 'application/json' # TODO necessary?
