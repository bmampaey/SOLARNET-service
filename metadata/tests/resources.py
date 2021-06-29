from metadata.resources.base_metadata import BaseMetadataResource
from .models import BaseMetadataTest

__all__ = ['BaseMetadataTestResource']

class BaseMetadataTestResource(BaseMetadataResource):
	'''RESTful resource for testing BaseMetadata abstract resource using model BaseMetadataTest'''
	
	class Meta(BaseMetadataResource.Meta):
		abstract = False
		queryset = BaseMetadataTest.objects.all()
		resource_name = 'base_metadata_test_resource'
