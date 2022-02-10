# Generated by command write_metadata_files version 1
from metadata.models import UsetWhiteLightLevel1
from .base_metadata import BaseMetadataResource

__all__ = ['UsetWhiteLightLevel1Resource']


class UsetWhiteLightLevel1Resource(BaseMetadataResource):
	'''RESTful resource for model UsetWhiteLightLevel1'''
	
	class Meta(BaseMetadataResource.Meta):
		abstract = False
		queryset = UsetWhiteLightLevel1.objects.all()
		resource_name = 'metadata_uset_white_light_level_1'