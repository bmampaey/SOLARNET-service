from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class DatasetCharacteristic(TaggedItemBase):
	content_object = models.ForeignKey('Dataset')
	
	class Meta(TaggedItemBase.Meta):
		db_table = "dataset_characteristic"

class Dataset(models.Model):
	name = models.TextField("Data set name.", max_length=20)
	description = models.TextField("Dataset description", blank=True, null=True)
	contact = models.TextField(help_text = "Contact email for the data set.", blank=True, null=True, max_length=50)
	instrument = models.TextField(help_text = "The instrument.", blank=True, null=True, max_length=20)
	telescope = models.TextField(help_text = "The telescope.", blank=True, null=True, max_length=20)
	characteristics = TaggableManager(through=DatasetCharacteristic)
	
	
	class Meta:
		db_table = "dataset"
		ordering = ["name"]
		verbose_name = "Dataset"
		verbose_name_plural = "Datasets"
	
	def __unicode__(self):
		return unicode(self.name)
