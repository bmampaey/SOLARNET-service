# Generated by command write_metadata_files version 1
from metadata.models import ChrotelLevel1
from .base_metadata import BaseMetadataResource

__all__ = ['ChrotelLevel1Resource']


class ChrotelLevel1Resource(BaseMetadataResource):
	'''RESTful resource for model ChrotelLevel1'''
	
	class Meta(BaseMetadataResource.Meta):
		abstract = False
		queryset = ChrotelLevel1.objects.all()
		resource_name = 'metadata_chrotel_level_1'
