
from rest_framework import serializers

from .models import Metadata
from dataset.serializers import DataLocationSerializer

class MetadataSerializer(serializers.HyperlinkedModelSerializer):
	data_location = DataLocationSerializer()
	class Meta:
		model = Metadata
		extra_kwargs = {'uri': {'lookup_field': 'oid'}}
