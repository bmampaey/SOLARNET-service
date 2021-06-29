from urllib.parse import unquote
from tastypie import fields
from tastypie.resources import ModelResource

from dataset.models import Characteristic
from api.constants import FILTERS
from .meta import ResourceMeta

__all__ = ['CharacteristicResource']

def datasets_use_in(bundle):
	'''Callable for the use_in parameter of the datasets ApiField of the CharacteristicResource'''
	# The characteristics ToManyField of DatasetResource has full=True
	# so only display the related datasets of the characteristic, if the request was not originally for a dataset resource
	try:
		return bundle.request.resolver_match.kwargs['resource_name'] != 'dataset'
	except (KeyError, AttributeError):
		return True

class CharacteristicResource(ModelResource):
	'''RESTful resource for model Characteristic'''
	
	datasets = fields.ToManyField('dataset.resources.DatasetResource', 'datasets', use_in=datasets_use_in)
	
	class Meta(ResourceMeta):
		queryset = Characteristic.objects.all()
		resource_name = 'characteristic'
		filtering = {
			'name': FILTERS.TEXT,
			'datasets': FILTERS.RELATIONAL,
		}
		ordering = ['name']
	
	def get_via_uri(self, uri, request=None):
		'''Pull apart the salient bits of the URI and populates the resource via a obj_get'''
		# HACK: There is a BUG in tastypie which affect resource URI with spaces and special characteristics
		# the method get_resource_uri use django.urls.reverse to convert a ressource to it's URI
		# and reverse quotes the returned URI, but get_via_uri does not unquote it first
		return super().get_via_uri(unquote(uri), request)
