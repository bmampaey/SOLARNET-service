from tastypie.api import Api

__all__ = ['SvoApi']

class SvoApi(Api):
	'''API for the SVO that improves the registration by allowing lookup by the model and saves a reference to the api on the resource'''
	
	title = 'SOLARNET Virtual Observatory RESTful API'
	description = 'Catalog of solar metadata accessible through a RESTful API'
	version = '2'
	basePath = '/api'
	
	def register(self, resource, canonical=True):
		super().register(resource, canonical)
		resource._meta.api = self
		self._canonicals[resource._meta.object_class] = resource
