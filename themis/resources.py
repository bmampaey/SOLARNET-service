from common.resources import BaseMetadaResource
from themis.models import Metadata


class MetadaResource(BaseMetadaResource):
	
	class Meta(BaseMetadaResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'themis_metadata'
