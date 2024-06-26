# Generated by command write_metadata_files version 1
from metadata.models import AiaLevel15
from .base_metadata import BaseMetadataResource

__all__ = ['AiaLevel15Resource']


class AiaLevel15Resource(BaseMetadataResource):
	'''RESTful resource for model AiaLevel15'''
	
	class Meta(BaseMetadataResource.Meta):
		abstract = False
		queryset = AiaLevel15.objects.all()
		resource_name = 'metadata_aia_level_1_5'
