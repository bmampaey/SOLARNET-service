from api.authentications import ApiKeyOrAnonymousAuthentication
from api.authorizations import AlwaysReadAuthorization
from api.serializers import Serializer

__all__ = ['ResourceMeta']

class ResourceMeta:
	'''Base class to set common parameters to all dataset resources'''
	# By default data provider cannot modify the dataset resources
	allowed_methods = ['get']
	# When requesting to create/update 1 or more objects, return the objects in the response
	always_return_data = True
	authentication = ApiKeyOrAnonymousAuthentication()
	authorization = AlwaysReadAuthorization()
	# Disable the hard max limit as the number of dataset resources will remain fairly small
	max_limit = None
	serializer = Serializer()
