
from django.db import models
from dataset.models import DataLocation

class Tag(models.Model):
	'''Metadata tag model'''
	name = models.TextField(primary_key=True, max_length=255, blank=False, null=False)
			
	def __unicode__(self):
		return str(self.name)

class BaseMetadata(models.Model):
	'''Model for the common fields of Metadata models'''
	oid = models.TextField('Observation ID', help_text = 'Unique identification string for the observation metadata, usually in the form YYYYMMDDHHMMSS', unique=True, db_index=True)
	fits_header = models.TextField(null=False, blank=True)
	data_location = models.ForeignKey(DataLocation, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.SET_NULL)
	tags = models.ManyToManyField(Tag, related_name='%(app_label)s_%(class)s', blank=True)
	date_beg = models.DateTimeField('DATE-BEG', help_text='Start time of the observation [UTC]', blank=True, null=True, db_index=True)
	date_end = models.DateTimeField('DATE-END', help_text='End time of the observation [UTC]', blank=True, null=True, db_index=True)
	wavemin = models.FloatField('WAVEMIN', help_text='Min value of the observation spectral range [nm]', blank=True, null=True, db_index=True)
	wavemax = models.FloatField('WAVEMAX', help_text='Max value of the observation spectral range [nm]', blank=True, null=True, db_index=True)
	
	class Meta:
		abstract = True
		ordering = ['date_beg']
	
	def __unicode__(self):
		return str(self.oid)
	
	@property
	def tags_names(self):
		return self.tags.values_list('name', flat=True)
