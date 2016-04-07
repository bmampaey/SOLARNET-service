from tastypie.authentication import Authentication
from django.contrib.auth.models import AnonymousUser
from web_account.models import User

class ApiKeyAuthentication(Authentication):
	''' Similar to Tastypie ApiKeyAuthentication but with web account user model '''
	auth_type = 'apikey'
	
	def anonymous(self, request):
		request.user = AnonymousUser()
		return True
	
	def extract_credentials(self, request):
		try:
			data = self.get_authorization_data(request)
		except ValueError:
			username = request.GET.get('username') or request.POST.get('username')
			api_key = request.GET.get('api_key') or request.POST.get('api_key')
		else:
			username, api_key = data.split(':', 1)
		
		return username, api_key
		
	def is_authenticated(self, request, **kwargs):
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
		
		if user.api_key == api_key:
			request.user = user
			return True
		else:
			return False

	def get_identifier(self, request):
		try:
			username = self.extract_credentials(request)[0]
		except ValueError:
			username = 'anonymous'
		return username
