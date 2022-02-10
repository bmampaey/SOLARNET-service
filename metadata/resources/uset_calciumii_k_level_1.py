# Generated by command write_metadata_files version 1
from metadata.models import UsetCalciumiiKLevel1
from .base_metadata import BaseMetadataResource

__all__ = ['UsetCalciumiiKLevel1Resource']


class UsetCalciumiiKLevel1Resource(BaseMetadataResource):
	'''RESTful resource for model UsetCalciumiiKLevel1'''
	
	class Meta(BaseMetadataResource.Meta):
		abstract = False
		queryset = UsetCalciumiiKLevel1.objects.all()
		resource_name = 'metadata_uset_calciumii_k_level_1'