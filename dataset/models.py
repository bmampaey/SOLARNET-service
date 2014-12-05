from django.db import models
from common.models import BaseMetaData, BaseDataLocation, BaseTag
from common.views import BaseSearchDataForm


class Dataset(models.Model):
	name = models.TextField("Dataset name.", primary_key=True, max_length=20)
	display_name = models.TextField("Dataset display name.", unique = True, blank=False, null=True, max_length=40)
	description = models.TextField("Dataset description", blank=True, null=True)
	contact = models.TextField(help_text = "Contact email for the data set.", blank=True, null=True, max_length=50)
	instrument = models.TextField(help_text = "The instrument.", blank=True, null=True, max_length=20)
	telescope = models.TextField(help_text = "The telescope.", blank=True, null=True, max_length=20)
	characteristics = models.ManyToManyField('Characteristic', related_name = "datasets")
	
	
	class Meta:
		db_table = "dataset"
		ordering = ["name"]
		verbose_name = "Dataset"
		verbose_name_plural = "Datasets"
	
	def __unicode__(self):
		return unicode(self.name)
	
	def __set_models(self):
		meta_data_models = dict((model._meta.app_label, model) for model in BaseMetaData.__subclasses__())
		if self.name in meta_data_models:
			self.__meta_data_model = meta_data_models[self.name]
		else:
			raise Exception("No MetaData model with name %s" % self.name)
		
		data_location_models = dict((model._meta.app_label, model) for model in BaseDataLocation.__subclasses__())
		if self.name in data_location_models:
			self.__data_location_model = data_location_models[self.name]
		else:
			raise Exception("No DataLocation model with name %s" % self.name)
		
		tag_models = dict((model._meta.app_label, model) for model in BaseTag.__subclasses__())
		if self.name in tag_models:
			self.__tag_model = tag_models[self.name]
		else:
			raise Exception("No Tag model with name %s" % self.name)
		
		search_data_forms = dict((form.dataset_name, form) for form in BaseSearchDataForm.__subclasses__())
		if self.name in search_data_forms:
			self.__search_data_form = search_data_forms[self.name]
		else:
			raise Exception("No SearchDataForm view with name %s" % self.name)
	
	@property
	def meta_data_model(self):
		if not hasattr(self, '__meta_data_model'):
			self.__set_models()
		return self.__meta_data_model
	
	@property
	def data_location_model(self):
		if not hasattr(self, '__data_location_model'):
			self.__set_models()
		return self.__data_location_model
	
	@property
	def tag_model(self):
		if not hasattr(self, '__tag_model'):
			self.__set_models()
		return self.__tag_model
	
	@property
	def search_data_form(self):
		if not hasattr(self, '__search_data_form'):
			self.__set_models()
		return self.__search_data_form
	
	@property
	def characteristics_names(self):
		return self.characteristics.values_list('name', flat=True)

class Characteristic(models.Model):
	name = models.TextField(primary_key=True, blank=False, null=False)
	
	class Meta:
		db_table = "characteristic"
	
	def __unicode__(self):
		return unicode(self.name)
