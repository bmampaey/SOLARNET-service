from common.resources import BaseMetadataResource
from swap_lev1.models import Metadata


class MetadataResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'swap_lev1_metadata'
