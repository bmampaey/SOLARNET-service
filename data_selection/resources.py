from django.forms import modelform_factory
from django.urls import reverse, NoReverseMatch
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.validation import FormValidation
from tastypie.exceptions import NotRegistered

from api.constants import FILTERS
from api.serializers import Serializer
from data_selection.models import DataSelection
from data_selection.authorizations import OwnerAuthorization
from metadata.utils import get_metadata_queryset

__all__ = ['DataSelectionResource']

class DataSelectionResource(ModelResource):
	'''RESTful resource for model DataSelection'''
	
	dataset = fields.ToOneField('dataset.resources.DatasetResource', 'dataset', full=True)
	zip_download_url = fields.CharField(attribute = 'zip_download_url', readonly = True, help_text = 'A URL to download the data selection as a ZIP archive')
	ftp_download_url = fields.CharField(attribute = 'ftp_download_url', readonly = True, help_text = 'A URL to download the data selection via FTP')
	# Object containing the metadata resource URI with an appropriate query string and the estimated number of items that would be returned if fetching that URI
	metadata = fields.DictField(readonly=True, help_text = 'The URI and the estimated count for the metadata of the data selection with current filters applied')
	
	class Meta:
		queryset = DataSelection.objects.all()
		resource_name = 'data_selection'
		filtering = {
			'dataset' : FILTERS.RELATIONAL,
			'creation_time' : FILTERS.DATETIME,
			'description': FILTERS.TEXT
		}
		ordering = ['-creation_time']
		# Allow only methods corresponding to create/read on the list URL and read/update/delete on the detail URL
		list_allowed_methods = ['post', 'get']
		detail_allowed_methods = ['get', 'patch', 'delete']
		# When requesting to create/update 1 or more objects, return the objects in the response
		always_return_data = True
		# Don't use the ApiKeyOrAnonymousAuthentication because user must be authenticated to access the data selection resource
		authentication = ApiKeyAuthentication()
		# Special authorization that allows user to only read/add/modify/delete their own data selections
		authorization = OwnerAuthorization()
		# Disable the hard max limit as the number of data selection will remain fairly small
		max_limit = None
		# The uuid field is for internal use only, don't expose it
		excludes = ['id', 'uuid']
		serializer = Serializer()
		# Validate data on submission
		validation = FormValidation(form_class = modelform_factory(DataSelection, exclude=excludes))
	
	def obj_create(self, bundle, **kwargs):
		# Make sure that new data selections belong to the autenthicated user
		return super().obj_create(bundle, owner=bundle.request.user)
	
	def dehydrate_metadata(self, bundle):
		'''Return the value for the metadata DictField or None if does not exist'''
		
		# Get the metadata model and the corresponding resource for the dataset
		try:
			metadata_model = bundle.obj.dataset.metadata_model
		except ValueError:
			return None
		
		try:
			metadata_resource = self._meta.api.canonical_resource_for(metadata_model)
		except NotRegistered:
			return None
		
		# Get the URI of the metadata resource and add the query string
		try:
			resource_uri = reverse('api_dispatch_list', kwargs={'resource_name': metadata_resource._meta.resource_name, 'api_name': metadata_resource._meta.api_name})
		except NoReverseMatch:
			return None
		
		if bundle.obj.query_string:
			resource_uri += '?' + bundle.obj.query_string
		
		# Get the metadata query set corresponding to the query string to compute the estimated count
		metadata = get_metadata_queryset(metadata_model, bundle.obj.query_string, bundle.obj.owner)
		
		return {
			'resource_uri': resource_uri,
			'count': metadata.count()
		}
