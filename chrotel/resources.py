from common.resources import BaseMetadaResource
from chrotel.models import Metadata


class MetadaResource(BaseMetadaResource):
	
	class Meta(BaseMetadaResource.Meta):
		queryset = Metadata.objects.all()
		resource_name = 'chrotel_metadata'
