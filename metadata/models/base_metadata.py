from django.db import models
from django.utils.functional import cached_property

__all__ = ['BaseMetadata']

class MetadataManager(models.Manager):
	'''Manager that optimize the queries by selecting the foreign objects'''
	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.select_related('data_location').prefetch_related('tags')
		return queryset


class BaseMetadata(models.Model):
	'''Abstract base model for the Metadata models'''
	oid = models.TextField('Observation ID', help_text = 'Unique identification string for the observation metadata, usually in the form YYYYMMDDHHMMSS; cannot be modified once it is set', unique=True, db_index=True)
	data_location = models.ForeignKey('dataset.DataLocation', related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.SET_NULL)
	tags = models.ManyToManyField('metadata.Tag', related_name='%(app_label)s_%(class)s', blank=True)
	date_beg = models.DateTimeField('DATE-BEG', help_text='Start time of the observation [UTC]', blank=True, null=True, db_index=True)
	date_end = models.DateTimeField('DATE-END', help_text='End time of the observation [UTC]', blank=True, null=True, db_index=True)
	wavemin = models.FloatField('WAVEMIN', help_text='Min value of the observation spectral range [nm]', blank=True, null=True, db_index=True)
	wavemax = models.FloatField('WAVEMAX', help_text='Max value of the observation spectral range [nm]', blank=True, null=True, db_index=True)
	
	objects = MetadataManager()
	
	class Meta:
		abstract = True
		ordering = ['date_beg']
	
	def __str__(self):
		return self.oid
	
	@cached_property
	def tags_names(self):
		return self.tags.values_list('name', flat=True)
