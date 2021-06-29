# Generated by command write_metadata_files version 1
from metadata.models import Rosa
from .base_metadata import BaseMetadataResource

__all__ = ['RosaResource']


class RosaResource(BaseMetadataResource):
	'''RESTful resource for model Rosa'''
	
	class Meta(BaseMetadataResource.Meta):
		abstract = False
		queryset = Rosa.objects.all()
		resource_name = 'metadata_rosa'
