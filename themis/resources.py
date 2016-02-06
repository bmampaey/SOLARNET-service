from common.resources import BaseMetadataResource
from themis.models import Metadata


class MetadataResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'themis_metadata'
