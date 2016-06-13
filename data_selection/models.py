from __future__ import unicode_literals
import urlparse

from django.db import models
from django.db.models.functions import Now
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import DEFAULT_DB_ALIAS

from picklefield.fields import PickledObjectField
from web_account.models import User
from dataset.models import Dataset

class DataSelectionGroup(models.Model):
	user = models.ForeignKey(User, related_name = 'data_selection_groups', related_query_name = 'data_selection_group', on_delete=models.CASCADE)
	name = models.CharField('Name of the data selection group', max_length = 80, null=False, blank=False)
	created = models.DateTimeField('Date of creation', null=False, blank=False)
	updated = models.DateTimeField('Date of last update', null=False, blank=False)
	
	class Meta:
		ordering = ['-updated']
		get_latest_by = 'updated'
		unique_together = (('user', 'name'),)
		db_table = 'data_selection_group'
		
	def __unicode__(self):
		return u'%s by %s on %s' % (self.name, self.user.get_username(), self.created)
	
	def save(self, *args, **kwargs):
		# Update the updated time
		self.updated = Now()
		
		# Set created time if it is not yet set
		if self.pk is None:
			self.created = Now()
		
		super(DataSelectionGroup, self).save(*args, **kwargs)
	
	@property
	def number_items(self):
		return sum(data_selection.number_items for data_selection in self.data_selections.all())

	
	@property
	def datasets(self):
		return self.data_selections.values_list('dataset', flat=True).distinct()
	
	@property
	def ftp_link(self):
		return urlparse.urljoin(settings.FTP_URL, '{self.user.id}/{self.name}/'.format(self = self))
	
	@property
	def metadata(self):
		metadata = dict()
		for data_selection in self.data_selections.all():
			if data_selection.dataset in metadata:
				metadata[data_selection.dataset] |= data_selection.metadata
			else:
				metadata[data_selection.dataset] = data_selection.metadata
		return metadata


class DataSelection(models.Model):
	data_selection_group = models.ForeignKey(DataSelectionGroup, related_name = 'data_selections', on_delete=models.CASCADE) # If the DataSelectionGroup is deleted, delete also the DataSelection
	dataset = models.ForeignKey(Dataset, related_name = 'data_selections', related_query_name = 'data_selection', on_delete=models.CASCADE)
	created = models.DateTimeField('Date of creation', null=False, blank=False, auto_now_add=True)
	number_items = models.IntegerField('Number of items in the data selection', null=True, blank=True)
	query_string = models.TextField('Query string for the data selection', null=True, blank=True)
	query = PickledObjectField('Django QuerySet query') # See https://docs.djangoproject.com/en/1.9/ref/models/querysets/#pickling-querysets
	
	class Meta:
		db_table = 'data_selection'
		
	def __unicode__(self):
		return u'%s for %s' % (self.dataset, self.data_selection_group)
	
	def save(self, *args, **kwargs):
		# Update the counter
		self.number_items = self.metadata.count()
		super(DataSelection, self).save(*args, **kwargs)
		
		# Update the data selection's group updated field
		self.data_selection_group.updated = self.created
		self.data_selection_group.save()
	
	@property
	def metadata(self):
		queryset = self.dataset.metadata_model.objects.all()
		queryset.query = self.query
		return queryset

