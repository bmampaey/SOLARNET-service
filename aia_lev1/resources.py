from common.resources import BaseMetadaResource
from aia_lev1.models import Metadata


class MetadaResource(BaseMetadaResource):
	
	class Meta(BaseMetadaResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'aia_lev1_metadata'
