from tastypie.exceptions import Unauthorized

from api.authorizations import AlwaysReadAuthorization

__all__ = ['DataLocationAuthorization']

class DataLocationAuthorization(AlwaysReadAuthorization):
	'''Authorisation that checks that the user is in the group related to the dataset of the data location being created/updated/deleted'''
	
	# HACK DataLocationResource only allow to modify a single object at a time, so we can just override perm_obj_checks
	def perm_obj_checks(self, request, code, obj):
		'''Test if the user of the request has the requested permission on the object'''
		
		auth_result = super().perm_obj_checks(request, code, obj)
		try:
			if request.user.groups.filter(pk = obj.dataset.user_group.pk).exists():
				return auth_result
		except AttributeError as why:
			pass
		raise Unauthorized('You are not allowed to access that resource')
