from SDA.authorizations import AlwaysReadAuthorization
from tastypie.authentication import MultiAuthentication, SessionAuthentication


class AnonymousGETAuthentication(SessionAuthentication):
	''' No authentication on GET '''
	
	def is_authenticated(self, request, **kwargs):
		''' If GET, don't check authentication, otherwise fall back to parent '''
		if request.method == "GET":
			return True
		else:
			return super(AnonymousGETAuthentication, self).is_authenticated(request, **kwargs)

class ResourceMeta:
	"""Base class to set common parameters to all resources"""
	max_limit = 100
	authentication = MultiAuthentication(SessionAuthentication(), AnonymousGETAuthentication())
	authorization = AlwaysReadAuthorization()
	always_return_data = True
	default_format = 'application/json' # TODO necessary?
