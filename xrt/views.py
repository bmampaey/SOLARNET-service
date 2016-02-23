from dataset.views import BaseMetadataViewSet
from .models import Metadata


class ChrotelMetadataViewSet(BaseMetadataViewSet):
	model = Metadata
