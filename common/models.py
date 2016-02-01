from __future__ import unicode_literals
from django.db import models
from django.core.validators import URLValidator

class DataLocation(models.Model):
	'''Data location model''' 
	url = models.TextField(help_text = "URL of the data at the remote site.", max_length=255, blank=True, null=True, validators = [URLValidator()])
	size = models.IntegerField(help_text = "Size of the data in bytes.", default=0, blank=True, null=True)
	thumbnail = models.TextField(help_text = "URL of the thumbnail at the remote site.", max_length=255, blank=True, null=True, default = None, validators = [URLValidator()])
	updated = models.DateTimeField(help_text = "Date of last update", null=False, blank=False, auto_now=True)
	
	class Meta:
		db_table = "data_location"
	
	def __unicode__(self):
		return unicode(self.file_url)


class Tag(models.Model):
	'''Metadata tag model'''
	name = models.TextField(primary_key=True, max_length=255, blank=False, null=False)
	
	class Meta:
		db_table = "tag"
			
	def __unicode__(self):
		return unicode(self.name)


class BaseMetadata(models.Model):
	'''Model for the common fields of Metadata models'''
	oid = models.BigIntegerField('Observation ID', help_text = 'Unique number for the observation metadata, usually in the form YYYYMMDDHHMMSS', unique = True)
	fits_header = models.TextField(null=False, blank=True)
	data_location = models.ForeignKey(DataLocation, related_name="%(app_label)s_%(class)s", null=True, blank=True, on_delete=models.SET_NULL)
	tags = models.ManyToManyField(Tag, related_name="%(app_label)s_%(class)s")
	
	class Meta:
		abstract = True
	
	def __unicode__(self):
		return unicode(self.id)
	
	@property
	def tags_names(self):
		return self.tags.values_list('name', flat=True)
