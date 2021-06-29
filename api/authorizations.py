from tastypie.authorization import DjangoAuthorization

__all__ = ['AlwaysReadAuthorization']

class AlwaysReadAuthorization(DjangoAuthorization):
	'''Authorisation similar to DjangoAuthorization, i.e it checks if the user has read/write/delete permission, but always allow read whoever the user is'''
	READ_PERM_CODE = 'view'
	
	def read_list(self, object_list, bundle):
		'''Returns a list of all the objects a user is allowed to read'''
		# Returning the complete object_list means that any user can fetch any object of the resource
		return object_list
	
	def read_detail(self, object_list, bundle):
		'''Returns either True if the user is allowed to read the object in question or throw Unauthorized if they are not'''
		# Returning True means that any user can fetch any object of the resource
		return True
