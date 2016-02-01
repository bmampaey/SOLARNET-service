from django.db import models
from django.core.validators import RegexValidator
from common.views import BaseSearchDataForm


class Telescope(models.Model):
	name = models.TextField(primary_key=True, blank=False, null=False, max_length = 20)
	description = models.TextField(help_text = "Telescope description", blank=True, null=True)
	
	def __unicode__(self):
		return unicode(self.name)

class Instrument(models.Model):
	name = models.TextField(primary_key=True, blank=False, null=False, max_length = 20)
	description = models.TextField(help_text = "Instrument description", blank=True, null=True)
	telescope = models.ForeignKey(Telescope, related_name = 'instruments', on_delete = models.DO_NOTHING)
	
	def __unicode__(self):
		return unicode(self.name)

class Characteristic(models.Model):
	name = models.TextField(primary_key=True, blank=False, null=False)
	
	def __unicode__(self):
		return unicode(self.name)

class Dataset(models.Model):
	id = models.TextField("Dataset name.", primary_key=True, max_length=20)
	name = models.TextField("Dataset display name.", unique = True, blank=False, null=False, max_length=40)
	description = models.TextField("Dataset description", blank=True, null=True)
	contact = models.TextField(help_text = "Contact email for the data set.", blank=True, null=True, max_length=50)
	telescope = models.ForeignKey(Telescope, db_column = "telescope", related_name = "datasets", on_delete = models.DO_NOTHING)
	instrument = models.ForeignKey(Instrument, db_column = "instrument", related_name = "datasets", on_delete = models.DO_NOTHING)
	characteristics = models.ManyToManyField(Characteristic, related_name = "datasets")
	_metadata_model = models.OneToOneField('ContentType', help_text='The model for this dataset metadata', blank=True, null=True, on_delete=models.SET_NULL)
	
	class Meta:
		db_table = "dataset"
		ordering = ["name"]
		verbose_name = "Dataset"
		verbose_name_plural = "Datasets"
	
	def __unicode__(self):
		return unicode(self.name)
	
	@property
	def metadata_model(self):
		if _metadata_model is None:
			raise Exception("No Matadata model has been set for this dataset")
		else:
			return self._metadata_model.model_class()
	
	@property
	def search_data_form(self):
		if not hasattr(self, '__search_data_form'):
			search_data_forms = dict((view.dataset_id, view.search_form_class) for view in BaseSearchDataForm.__subclasses__())
			if self.id in search_data_forms:
				self.__search_data_form = search_data_forms[self.id]
			else:
				raise Exception("No SearchDataForm view for dataset %s" % self.id)
		return self.__search_data_form
	
	@property
	def characteristics_names(self):
		return self.characteristics.values_list('name', flat=True)


class Keyword(models.Model):
	PYTHON_TYPE_CHOICES = (
		("str", "string"),
		("bool", "bool"),
		("int", "int"),
		("float", "float"),
		("datetime", "datetime (iso format)"),
	)
	db_column = models.TextField("Column name of the corresponding keyword in the meta_data table.", blank=False, null=False, max_length=30, primary_key = True, validators=RegexValidator(r"^[a-z][_a-z]*$"))
	name = models.CharField(help_text = "Fits like name of the keyword. Can contain space and dashes.", blank=False, null=False, max_length=70)
	python_type = models.CharField(help_text = "Python type of the keyword.", blank=False, null=False, max_length=12, default = "string", choices = PYTHON_TYPE_CHOICES)
	unit = models.CharField(help_text = "Physical unit (SI compliant) of the keyword.", blank=True, null=True, max_length=10)
	description = models.TextField(help_text = "Full description of the keyword.", blank=True, null=True, max_length=70)
	dataset = models.ForeignKey(Dataset, db_column = "dataset", related_name = "keywords", on_delete = models.DO_NOTHING)
	
	def __unicode__(self):
		return unicode(self.name)
