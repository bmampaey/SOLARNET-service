from common.resources import BaseMetadaResource
from swap_lev1.models import Metadata


class MetadaResource(BaseMetadaResource):
	
	class Meta(BaseMetadaResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'swap_lev1_metadata'
