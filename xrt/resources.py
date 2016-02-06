from common.resources import BaseMetadataResource
from xrt.models import Metadata


class MetadataResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'xrt_metadata'
