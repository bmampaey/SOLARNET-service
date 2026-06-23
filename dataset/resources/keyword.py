from tastypie import fields
from tastypie.resources import ModelResource

from api.filters import FILTERS, get_relational_filters
from dataset.models import Keyword
from dataset.resources import DatasetResource

from .meta import ResourceMeta

__all__ = ['KeywordResource']


class KeywordResource(ModelResource):
	"""RESTful resource for model Keyword"""

	dataset = fields.ToOneField('dataset.resources.DatasetResource', 'dataset')

	class Meta(ResourceMeta):
		queryset = Keyword.objects.all()
		resource_name = 'keyword'
		filtering = {
			'dataset': get_relational_filters(DatasetResource),
			'name': FILTERS.TEXT,
			'verbose_name': FILTERS.TEXT,
			'type': FILTERS.TEXT,
			'unit': FILTERS.TEXT,
			'description': FILTERS.TEXT,
		}
		ordering = ['dataset', 'name', 'verbose_name', 'type', 'unit', 'description']
