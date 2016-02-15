
from rest_framework import viewsets

from .models import Metadata
from .serializers import MetadataSerializer

class MetadataViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Metadata.objects.all()
	serializer_class = MetadataSerializer
	lookup_field = 'oid'
