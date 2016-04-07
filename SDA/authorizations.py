from tastypie.authorization import ReadOnlyAuthorization, DjangoAuthorization
from tastypie.exceptions import Unauthorized


class AlwaysReadAuthorization(DjangoAuthorization):
	''' Always allow read, for the rest check Django permissions '''
	# This is necessary because django require change permission even for just reading
	def read_list(self, object_list, bundle):
		return object_list
	
	def read_detail(self, object_list, bundle):
		return True

class UserOnlyModifAuthorization(ReadOnlyAuthorization):
	''' Only user can update or delete it's own objects '''
	
	def __init__(self, user_field, *args, **kwargs):
		self.user_field = user_field
		super(UserOnlyModifAuthorization, self).__init__(*args, **kwargs)
	
	def create_list(self, object_list, bundle):
		if bundle.request.user.is_authenticated() and bundle.request.user.is_active:
			return object_list
		else:
			raise Unauthorized('You are not authenticated or active')
	
	def create_detail(self, object_list, bundle):
		return bundle.request.user.is_authenticated() and bundle.request.user.is_active
	
	def update_list(self, object_list, bundle):
		if bundle.request.user.is_authenticated() and bundle.request.user.is_active:
			return object_list.filter(**{self.user_field: bundle.request.user})
		else:
			raise Unauthorized('You are not authenticated or active')
	
	def update_detail(self, object_list, bundle):
		return bundle.request.user.is_authenticated() and bundle.request.user.is_active and getattr(bundle.obj, self.user_field) == bundle.request.user
	
	def delete_list(self, object_list, bundle):
		return self.update_list(object_list, bundle)
	
	def delete_detail(self, object_list, bundle):
		return self.update_detail(object_list, bundle)
