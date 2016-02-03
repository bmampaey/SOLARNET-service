from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import MultiAuthentication, BasicAuthentication, SessionAuthentication


class AnonymousGETAuthentication(BasicAuthentication):
	""" No authentication on GET """
	
	def is_authenticated(self, request, **kwargs):
		""" If GET, don't check authentication, otherwise fall back to parent """
	
		if request.method == "GET":
			return True
		else:
			return super(AnonymousGETAuthentication, self).is_authenticated(request, **kwargs)


class ResourceMeta:
	"""Base class to set common parameters to all resources"""
	max_limit = 100
	authentication = MultiAuthentication(SessionAuthentication(), AnonymousGETAuthentication())
	authorization = DjangoAuthorization()
	always_return_data = True
	default_format = 'application/json' # TODO necessary?
