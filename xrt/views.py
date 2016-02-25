from dataset.views import BaseMetadataViewSet
from .models import Metadata


class MetadataViewSet(BaseMetadataViewSet):
	model = Metadata
