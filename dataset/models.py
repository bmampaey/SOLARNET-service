
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator, EmailValidator, URLValidator
from django.core.exceptions import ValidationError

class DataLocation(models.Model):
	'''Data location model'''
	dataset = models.ForeignKey('Dataset', on_delete = models.DO_NOTHING, related_name = 'data_locations')
	file_url = models.TextField(help_text = 'URL of the data at the remote site', max_length=255, validators = [URLValidator()])
	file_size = models.BigIntegerField(help_text = 'Size of the data in bytes', default=0, blank=True, null=True)
	file_path = models.TextField(help_text = 'Path of the data at the local site', db_index=True, blank=True, null=True, validators = [RegexValidator(regex=r'^[^/]+(?:/[^/]+)*$')])
	thumbnail_url = models.TextField(help_text = 'URL of the thumbnail at the remote site', max_length=255, blank=True, null=True, default = None, validators = [URLValidator()])
	updated = models.DateTimeField(help_text = 'Date of last update', null=False, blank=False, auto_now=True)
	offline = models.BooleanField(help_text = 'The data is not available for download', null=False, blank=False, default=False)
	
	class Meta:
		db_table = 'data_location'
		unique_together = [('dataset', 'file_url')]
	
	def __unicode__(self):
		return str(self.file_url)

class Telescope(models.Model):
	name = models.TextField(primary_key=True, blank=False, null=False, max_length = 20)
	description = models.TextField(help_text = 'Telescope description', blank=True, null=True)
	
	def __unicode__(self):
		return str(self.name)

class Instrument(models.Model):
	name = models.TextField(primary_key=True, blank=False, null=False, max_length = 20)
	description = models.TextField(help_text = 'Instrument description', blank=True, null=True)
	telescope = models.ForeignKey(Telescope, related_name = 'instruments', on_delete = models.DO_NOTHING)
	
	def __unicode__(self):
		return str(self.name)

class Characteristic(models.Model):
	name = models.TextField(primary_key=True, blank=False, null=False)
	
	def __unicode__(self):
		return str(self.name)

class Dataset(models.Model):
	id = models.TextField('Dataset id', primary_key=True, max_length=20, validators=[RegexValidator(r'^[a-z][_a-z0-9]*$')], help_text='Must start with a lower case lettre, then only lower case letters, numbers and underscores are allowed')
	name = models.TextField('Dataset display name', unique = True, blank=False, null=False, max_length=40)
	description = models.TextField('Dataset description', blank=True, null=True)
	contact = models.TextField(help_text = 'Contact email for the data set', blank=True, null=True, max_length=50, validators=[EmailValidator()])
	telescope = models.ForeignKey(Telescope, db_column = 'telescope', related_name = 'datasets', on_delete = models.DO_NOTHING)
	instrument = models.ForeignKey(Instrument, db_column = 'instrument', related_name = 'datasets', on_delete = models.DO_NOTHING)
	archive_url = models.TextField(help_text = 'Official URL of the archive', max_length=255, blank=True, null=True, default = None, validators = [URLValidator()])
	characteristics = models.ManyToManyField(Characteristic, related_name = 'datasets', blank=True)
	_metadata_model = models.OneToOneField(ContentType, help_text='The model for this dataset metadata', blank=True, null=True, on_delete=models.SET_NULL)
	
	class Meta:
		db_table = 'dataset'
		ordering = ['name']
		verbose_name = 'Dataset'
		verbose_name_plural = 'Datasets'
	
	def __unicode__(self):
		return str(self.name)
	
	@property
	def metadata_model(self):
		if self._metadata_model is None:
			raise Exception('No Metadata model has been set for this dataset')
		else:
			return self._metadata_model.model_class()
	
	@property
	def characteristics_names(self):
		return self.characteristics.values_list('name', flat=True)


class Keyword(models.Model):
	PYTHON_TYPE_CHOICES = (
		('str', 'string'),
		('bool', 'bool'),
		('int', 'int'),
		('long', 'bigint'),
		('float', 'float'),
		('datetime', 'datetime (iso format)'),
	)
	dataset = models.ForeignKey(Dataset, db_column = 'dataset', related_name = 'keywords', on_delete = models.DO_NOTHING)
	db_column = models.TextField('Column name of the corresponding keyword in the metadata table', blank=False, null=False, max_length=30, validators=[RegexValidator(r'^[a-z][_a-z0-9]*$')])
	name = models.CharField(help_text = 'Fits like name of the keyword. Can contain space and dashes', blank=False, null=False, max_length=70)
	python_type = models.CharField(help_text = 'Python type of the keyword', blank=False, null=False, max_length=12, default = 'string', choices = PYTHON_TYPE_CHOICES)
	unit = models.CharField(help_text = 'Physical unit (SI compliant) of the keyword', blank=True, null=True, max_length=70)
	description = models.TextField(help_text = 'Full description of the keyword', blank=True, null=True, max_length=70)
	
	class Meta:
		ordering = ['dataset', 'db_column']
		unique_together = [('dataset', 'db_column'), ('dataset', 'name')]

	def __unicode__(self):
		return str(self.name)
