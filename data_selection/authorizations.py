from django.db.models.query import QuerySet
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

__all__ = ['OwnerAuthorization']

class OwnerAuthorization(Authorization):
	'''Only the owner can create/read/update/delete it's own objects'''
	
	def __init__(self, owner_field = 'owner', *args, **kwargs):
		self.owner_field = owner_field
		super().__init__(*args, **kwargs)
	
	def check_object_list(self, object_list, bundle):
		'''Return only the objects in the list that belong to the request user'''
		# Optimize the filtering if it is a queryset
		if isinstance(object_list, QuerySet):
			return object_list.filter(**{self.owner_field: bundle.request.user})
		else:
			return [getattr(object, self.owner_field, None) == bundle.request.user for object in object_list]
	
	def check_object(self, object, bundle):
		'''Return True if the object belong to the request user or throw Unauthorized if it doesnt'''
		if getattr(object, self.owner_field, None) == bundle.request.user:
			return True
		else:
			raise Unauthorized('You are not allowed to access that resource')
	
	def read_list(self, object_list, bundle):
		'''Returns a list of all the objects a user is allowed to read.'''
		return self.check_object_list(object_list, bundle)
	
	def read_detail(self, object_list, bundle):
		'''Returns either True if the user is allowed to read the object in question or throw Unauthorized if they are not'''
		return self.check_object(bundle.obj, bundle)
	
	def create_list(self, object_list, bundle):
		'''Unimplemented, as Tastypie never creates entire new lists, but present for consistency & possible extension'''
		raise NotImplementedError('Tastypie has no way to determine if all objects should be allowed to be created')
	
	def create_detail(self, object_list, bundle):
		'''Returns either True if the user is allowed to create the object in question or throw Unauthorized if they are not'''
		return self.check_object(bundle.obj, bundle)
	
	def update_list(self, object_list, bundle):
		'''Returns a list of all the objects a user is allowed to update'''
		return self.check_object_list(object_list, bundle)
	
	def update_detail(self, object_list, bundle):
		'''Returns either True if the user is allowed to update the object in question or throw Unauthorized if they are not'''
		return self.check_object(bundle.obj, bundle)
	
	def delete_list(self, object_list, bundle):
		'''Returns a list of all the objects a user is allowed to delete'''
		return self.check_object_list(object_list, bundle)
	
	def delete_detail(self, object_list, bundle):
		'''Returns either True if the user is allowed to delete the object in question or throw Unauthorized if they are not'''
		return self.check_object(bundle.obj, bundle)
