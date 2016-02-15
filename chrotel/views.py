from rest_framework import viewsets

from chrotel.models import Metadata
from chrotel.serializers import MetadataSerializer

class MetadataViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows metadata to be viewed or edited.
	"""
	queryset = Metadata.objects.all()
	serializer_class = MetadataSerializer
	lookup_field = 'oid'
