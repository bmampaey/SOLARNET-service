# Generated by command write_metadata_files version 1
from metadata.models import Ibis
from .base_metadata import BaseMetadataResource

__all__ = ['IbisResource']


class IbisResource(BaseMetadataResource):
	'''RESTful resource for model Ibis'''
	
	class Meta(BaseMetadataResource.Meta):
		abstract = False
		queryset = Ibis.objects.all()
		resource_name = 'ibis'