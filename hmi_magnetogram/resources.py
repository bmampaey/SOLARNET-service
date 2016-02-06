from common.resources import BaseMetadataResource
from hmi_magnetogram.models import Metadata


class MetadataResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'hmi_magnetogram_metadata'
