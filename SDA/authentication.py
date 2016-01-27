from tastypie.authentication import MultiAuthentication, BasicAuthentication, SessionAuthentication

class AnonymousGETAuthentication(BasicAuthentication):
	""" No auth on GET """
	
	def is_authenticated(self, request, **kwargs):
		""" If GET, don't check auth, otherwise fall back to parent """
	
		if request.method == "GET":
			return True
		else:
			return super(AnonymousGETAuthentication, self).is_authenticated(request, **kwargs)

authentication = MultiAuthentication(SessionAuthentication(), AnonymousGETAuthentication())
