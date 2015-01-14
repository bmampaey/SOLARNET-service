from django.db import models
from common.models import BaseMetaData, BaseDataLocation, BaseTag
from common.views import BaseSearchDataForm

class Telescope(models.Model):
	name = models.TextField(primary_key=True, blank=False, null=False, max_length = 20)
	description = models.TextField(help_text = "Telescope description", blank=True, null=True)

	class Meta:
		db_table = "telescope"
	
	def __unicode__(self):
		return unicode(self.name)

class Instrument(models.Model):
	name = models.TextField(primary_key=True, blank=False, null=False, max_length = 20)
	description = models.TextField(help_text = "Instrument description", blank=True, null=True)
	telescope = models.ForeignKey(Telescope, related_name = 'instruments', on_delete = models.DO_NOTHING)
	
	class Meta:
		db_table = "instrument"
	
	def __unicode__(self):
		return unicode(self.name)

class Characteristic(models.Model):
	name = models.TextField(primary_key=True, blank=False, null=False)
	
	class Meta:
		db_table = "characteristic"
	
	def __unicode__(self):
		return unicode(self.name)

class Dataset(models.Model):
	id = models.TextField("Dataset name.", primary_key=True, max_length=20)
	name = models.TextField("Dataset display name.", unique = True, blank=False, null=True, max_length=40)
	description = models.TextField("Dataset description", blank=True, null=True)
	contact = models.TextField(help_text = "Contact email for the data set.", blank=True, null=True, max_length=50)
	telescope = models.ForeignKey(Telescope, db_column = "telescope", related_name = "datasets", on_delete = models.DO_NOTHING)
	instrument = models.ForeignKey(Instrument, db_column = "instrument", related_name = "datasets", on_delete = models.DO_NOTHING)
	characteristics = models.ManyToManyField(Characteristic, related_name = "datasets")
	
	
	class Meta:
		db_table = "dataset"
		ordering = ["name"]
		verbose_name = "Dataset"
		verbose_name_plural = "Datasets"
	
	def __unicode__(self):
		return unicode(self.name)
	
	def __set_models(self):
		meta_data_models = dict((model._meta.app_label, model) for model in BaseMetaData.__subclasses__())
		if self.id in meta_data_models:
			self.__meta_data_model = meta_data_models[self.id]
		else:
			raise Exception("No MetaData model for dataset %s" % self.id)
		
		data_location_models = dict((model._meta.app_label, model) for model in BaseDataLocation.__subclasses__())
		if self.id in data_location_models:
			self.__data_location_model = data_location_models[self.id]
		else:
			raise Exception("No DataLocation model for dataset %s" % self.id)
		
		tag_models = dict((model._meta.app_label, model) for model in BaseTag.__subclasses__())
		if self.id in tag_models:
			self.__tag_model = tag_models[self.id]
		else:
			raise Exception("No Tag model for dataset %s" % self.id)
		
		search_data_forms = dict((view.dataset_id, view.search_form_class) for view in BaseSearchDataForm.__subclasses__())
		if self.id in search_data_forms:
			self.__search_data_form = search_data_forms[self.id]
		else:
			raise Exception("No SearchDataForm view for dataset %s" % self.id)
	
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

