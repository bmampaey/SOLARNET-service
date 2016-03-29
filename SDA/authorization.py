from tastypie.authorization import DjangoAuthorization

class AlwaysReadAuthorization(DjangoAuthorization):
	''' Always allow read '''
	def read_list(self, object_list, bundle):
		return object_list
	
	def read_detail(self, object_list, bundle):
		return True
