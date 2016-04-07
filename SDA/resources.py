from SDA.authorizations import AlwaysReadAuthorization
from SDA.authentication import ApiKeyAuthentication

class ResourceMeta:
	'''Base class to set common parameters to all resources'''
	max_limit = 100
	authentication = ApiKeyAuthentication()
	authorization = AlwaysReadAuthorization()
	# Necessary for tastypie angular resource
	always_return_data = True

