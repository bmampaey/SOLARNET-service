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
			email = request.GET.get('email') or request.POST.get('email')
			api_key = request.GET.get('api_key') or request.POST.get('api_key')
		else:
			email, api_key = data.split(':', 1)
		
		return email, api_key
		
	def is_authenticated(self, request, **kwargs):
		
		try:
			email, api_key = self.extract_credentials(request)
		except ValueError:
			return self.anonymous(request)
		
		if not email or not api_key:
			return self.anonymous(request)
		
		try:
			user = User.objects.get(email = email)
		except User.DoesNotExist:
			return self.anonymous(request)
		
		if user.api_key == api_key:
			request.user = user
			return True
		else:
			return False
	
	def get_identifier(self, request):
		try:
			email, trash = self.extract_credentials(request)
		except ValueError:
			email = 'anonymous'
		return email
