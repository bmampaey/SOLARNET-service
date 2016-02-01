from django.db import models

class DataLocation(models.Model):
	'''Data location model''' 
	url = models.TextField(help_text = "URL of the data at the remote site.", max_length=255, blank=True, null=True)
	size = models.IntegerField(help_text = "Size of the data in bytes.", default=0, blank=True, null=True)
	thumbnail = models.TextField(help_text = "URL of the thumbnail at the remote site.", max_length=255, blank=True, null=True, default = None)
	updated = models.DateTimeField(help_text = "Date of last update", null=False, blank=False, auto_now=True)
	
	class Meta:
		db_table = "data_location"
	
	def __unicode__(self):
		return unicode(self.file_url)


class Tag(models.Model):
	'''Matadata tag model'''
	name = models.TextField(primary_key=True, max_length=255, blank=False, null=False)
	
	class Meta:
		db_table = "tag"
			
	def __unicode__(self):
		return unicode(self.name)
#	
#	@classmethod
#	def all_tags(cls):
#		tags = [sub_model.objects.values_list("name", flat=True) for sub_model in cls.__subclasses__()]
#		return set([t for ts in tags for t in ts])


class BaseMatadata(models.Model):
	'''Model for the common fields of Matadata models'''
	oid = models.BigIntegerField('Observation ID', help_text = 'Unique number for the observation metadata, usually in the form YYYYMMDDHHMMSS', unique = True)
	fits_header = models.TextField(null=False, blank=True)
	data_location = models.ForeignKey(DataLocation, related_name="%(app_label)s_%(class)s", on_delete=models.SET_NULL)
	tags = models.ManyToManyField(Tag, related_name="%(app_label)s_%(class)s")
	
	class Meta:
		abstract = True
	
	def __unicode__(self):
		return unicode(self.id)
	
	@property
	def tags_names(self):
		return self.tags.values_list('name', flat=True)
