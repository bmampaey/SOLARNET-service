import logging
import pprint

__all__ = ['RequestLoggingMiddleware']

class RequestLoggingMiddleware:
	'''Middleware that will log all POST/PUT/PATCH requests on the api to the requests logger'''
	
	def __init__(self, get_response):
		self.get_response = get_response
		self.logger = logging.getLogger('requests')
	
	def __call__(self, request):
		
		try:
			response = self.get_response(request)
		except Exception as why:
			self.logger.critical('%s %s\n%s\n%s', request.path, why, pprint.pformat(dict(request.headers), indent=2, width=300), request.POST or request.body)
			raise
		
		if self.check_method(request) and self.check_path(request):
			if response.status_code >= 400:
				self.logger.error('%s %s\n%s\n%s', request.path, response.status_code, pprint.pformat(dict(request.headers), indent=2, width=300), request.POST or request.body)
			else:
				self.logger.info('%s %s\n%s\n%s', request.path, response.status_code, pprint.pformat(dict(request.headers), indent=2, width=300), request.POST or request.body)
		
		return response
	
	def check_path(self, request):
		return request.path_info.startswith('/api/svo') and not request.path_info.startswith('/api/svo/user')
	
	def check_method(self, request):
		return request.method in ('POST', 'PATCH', 'PUT')
