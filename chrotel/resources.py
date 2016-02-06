from common.resources import BaseMetadataResource
from chrotel.models import Metadata


class MetadataResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'chrotel_metadata'
