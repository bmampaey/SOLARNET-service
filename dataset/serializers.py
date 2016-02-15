from rest_framework import serializers

from dataset.models import Telescope, Instrument, Characteristic, Dataset, Keyword, DataLocation, Tag

class InstrumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Instrument

class TelescopeSerializer(serializers.ModelSerializer):
	# Include all the instruments of the Telescope
	instruments = InstrumentSerializer(many=True)
	class Meta:
		model = Telescope

class DatasetSerializer(serializers.ModelSerializer):
	number_items = serializers.SerializerMethodField()
	class Meta:
		model = Dataset
		exclude = ['_metadata_model']
	
	def get_number_items(self, obj):
		# TODO add filtering
		# TODO add estimated count if too slow
		return obj.metadata_model.objects.count()

class CharacteristicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Characteristic

class KeywordSerializer(serializers.ModelSerializer):
	class Meta:
		model = Keyword

class DataLocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = DataLocation

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
