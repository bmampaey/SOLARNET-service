from common.resources import BaseMetadaResource
from hmi_magnetogram.models import Metadata


class MetadaResource(BaseMetadaResource):
	
	class Meta(BaseMetadaResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'hmi_magnetogram_metadata'
