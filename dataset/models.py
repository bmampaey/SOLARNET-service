from django.db import models

# Create your models here.

class DataSet(models.Model):
	name = models.CharField("Data set name.", max_length=20, primary_key = True)
	contact = models.CharField(help_text = "Contact email for the data set.", blank=True, null=True, max_length=50)
	instrument = models.CharField(help_text = "Contact email for the data set.", blank=False, null=False, max_length=70)
	euv = models.BooleanField(help_text = "Data is EUV.", default = False, blank=True)
	image = models.BooleanField(help_text = "Data are images.", default = False, blank=True)
	
	class Meta:
		db_table = "data_set"
		ordering = ["name"]
		verbose_name = "Data set"
		verbose_name_plural = "Data sets"
	
	def __unicode__(self):
		return unicode(self.name)
