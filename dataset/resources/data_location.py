from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation
from django.forms import modelform_factory, TypedChoiceField

from api.constants import FILTERS
from dataset.models import DataLocation
from dataset.authorizations import DataLocationAuthorization
from .meta import ResourceMeta

__all__ = ['DataLocationResource']

class DataLocationResource(ModelResource):
	'''RESTful resource for model DataLocation'''
	
	dataset = fields.ToOneField('dataset.resources.DatasetResource', 'dataset')
	
	class Meta(ResourceMeta):
		queryset = DataLocation.objects.all()
		resource_name = 'data_location'
		filtering = {
			'dataset': FILTERS.RELATIONAL,
			'file_url': FILTERS.TEXT,
			'file_size': FILTERS.NUMERIC,
			'file_path': FILTERS.TEXT,
			'thumbnail_url': FILTERS.TEXT,
			'update_time': FILTERS.DATETIME,
			'offline': FILTERS.BOOLEAN
		}
		ordering = ['dataset', 'file_url', 'file_size', 'file_path', 'thumbnail_url', 'update_time', 'offline']
		# Allow only methods corresponding to create/read on the list URL and read/update/delete on the detail URL
		list_allowed_methods = ['post', 'get']
		detail_allowed_methods = ['get', 'patch', 'delete']
		# Special authorization that allows data provider to only add/modify/delete data location for their dataset
		authorization = DataLocationAuthorization()
		# Limit the hard max on data location as there may be millions
		max_limit = 1000
		# Validate data on submission
		# HACK: override offline so that it only accepts True or False
		validation = FormValidation(form_class = modelform_factory(DataLocation, fields='__all__', field_classes = {'offline': lambda *args, **kwargs: TypedChoiceField(*args, choices = [(True, 'true'), (False, 'false')], **kwargs)}))
