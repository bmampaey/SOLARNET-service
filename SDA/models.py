from django.db import models

# Create your models here.

class Keyword(models.Model):
	PYTHON_TYPE_CHOICES = (
		("str", "string"),
		("bool", "bool"),
		("int", "int"),
		("float", "float"),
		("datetime", "datetime (iso format)"),
	)
	column = models.CharField("Column name of the corresponding keyword in the meta_data table.", max_length=30, primary_key = True)
	name = models.CharField(help_text = "Fits like name of the keyword. Can contain space and dashes.", blank=True, null=True, max_length=70)
	python_type = models.CharField(help_text = "Python type of the keyword.", blank=True, null=False, max_length=12, default = "string", choices = PYTHON_TYPE_CHOICES)
	unit = models.CharField(help_text = "Physical unit (SI compliant) of the keyword.", blank=True, null=True, max_length=10)
	description = models.CharField(help_text = "Full description of the keyword.", blank=True, null=True, max_length=70)
	
	class Meta:
		abstract = True
		db_table = "keyword"
	
	def __unicode__(self):
		return unicode(self.name)


class DataLocation(models.Model):
	
	path = models.CharField(help_text = "Path of the data at the data site.", max_length=255, blank=True, null=True)
	
	class Meta:
		abstract = True
		db_table = "data_location"
	
	def __unicode__(self):
		return unicode(self.path)
