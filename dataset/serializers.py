from rest_framework import serializers

from dataset.models import Telescope, Instrument, Characteristic, Dataset, Keyword
from dataset.models import DataLocation, Tag

class InstrumentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Instrument
		fields = ['url', 'name', 'description', 'telescope']

class TelescopeSerializer(serializers.HyperlinkedModelSerializer):
	# Include all the instruments of the Telescope
	instruments = InstrumentSerializer(many=True)
	class Meta:
		model = Telescope
		fields = ['url', 'name', 'description', 'instruments']

class DatasetSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Dataset

class CharacteristicSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Characteristic
		fields = ['url', 'name']

class KeywordSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Keyword

class DataLocationSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = DataLocation

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
#		fields = ['url', 'name']