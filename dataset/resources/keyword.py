from tastypie import fields
from tastypie.resources import ModelResource

from dataset.models import Keyword
from api.constants import FILTERS
from .meta import ResourceMeta

__all__ = ['KeywordResource']

class KeywordResource(ModelResource):
	'''RESTful resource for model Keyword'''
	
	dataset = fields.ToOneField('dataset.resources.DatasetResource', 'dataset')
	
	class Meta(ResourceMeta):
		queryset = Keyword.objects.all()
		resource_name = 'keyword'
		filtering = {
			'dataset': FILTERS.RELATIONAL,
			'name': FILTERS.TEXT,
			'verbose_name': FILTERS.TEXT,
			'type': FILTERS.TEXT,
			'unit': FILTERS.TEXT,
			'description': FILTERS.TEXT,
		}
		ordering = ['dataset', 'name', 'verbose_name', 'type', 'unit', 'description']
