from urllib.parse import unquote

from tastypie import fields
from tastypie.resources import ModelResource

from api.filters import FILTERS, get_relational_filters
from dataset.models import Instrument

from .meta import ResourceMeta
from .telescope import TelescopeResource

__all__ = ['InstrumentResource']


class InstrumentResource(ModelResource):
	"""RESTful resource for model Instrument"""

	telescope = fields.ToOneField('dataset.resources.TelescopeResource', 'telescope')

	class Meta(ResourceMeta):
		queryset = Instrument.objects.all()
		resource_name = 'instrument'
		filtering = {
			'name': FILTERS.TEXT,
			'description': FILTERS.TEXT,
			'telescope': get_relational_filters(TelescopeResource),
		}
		ordering = ['name', 'description', 'telescope']

	def get_via_uri(self, uri, request=None):
		"""Pull apart the salient bits of the URI and populates the resource via a obj_get"""
		# HACK: There is a BUG in tastypie which affect resource URI with spaces and special characteristics
		# the method get_resource_uri use django.urls.reverse to convert a ressource to it's URI
		# and reverse quotes the returned URI, but get_via_uri does not unquote it first
		return super().get_via_uri(unquote(uri), request)
