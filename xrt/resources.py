from common.resources import BaseMetadaResource
from xrt.models import Metadata


class MetadaResource(BaseMetadaResource):
	
	class Meta(BaseMetadaResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'xrt_metadata'
