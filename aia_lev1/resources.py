from common.resources import BaseMetadataResource
from aia_lev1.models import Metadata


class MetadataResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'aia_lev1_metadata'
