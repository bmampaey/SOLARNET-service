from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import MultiAuthentication, BasicAuthentication, SessionAuthentication


class AnonymousGETAuthentication(BasicAuthentication):
	''' No authentication on GET '''
	
	def is_authenticated(self, request, **kwargs):
		''' If GET, don't check authentication, otherwise fall back to parent '''
		
		if request.method == "GET":
			return True
		else:
			return super(AnonymousGETAuthentication, self).is_authenticated(request, **kwargs)

class AlwaysReadAuthorization(DjangoAuthorization):
	''' Always allow read '''
	def read_list(self, object_list, bundle):
		return object_list
	
	def read_detail(self, object_list, bundle):
		return True


class ResourceMeta:
	"""Base class to set common parameters to all resources"""
	max_limit = 100
	authentication = MultiAuthentication(SessionAuthentication(), AnonymousGETAuthentication())
	authorization = AlwaysReadAuthorization()
	always_return_data = True
	default_format = 'application/json' # TODO necessary?
