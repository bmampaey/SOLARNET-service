from uuid import uuid4
from django.conf import settings
from django.db import models
from django.urls import reverse

__all__ = ['DataSelection']


class DataSelectionManager(models.Manager):
	'''Manager that optimize the queries by selecting the foreign objects'''
	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.select_related('owner', 'dataset')
		return queryset


class DataSelection(models.Model):
	owner = models.ForeignKey('auth.User', related_name = 'data_selections', related_query_name = 'data_selection', on_delete=models.CASCADE)
	dataset = models.ForeignKey('dataset.Dataset', on_delete=models.CASCADE, related_name = 'data_selections', related_query_name = 'data_selection')
	query_string = models.TextField('Query string representing the dataset metadata selection', null=True, blank=True)
	description = models.TextField('Description for the data selection', null=True, blank=True)
	creation_time = models.DateTimeField('Date of creation', blank=True, auto_now_add=True)
	uuid = models.UUIDField('Unique identifier for web access', blank=True, default=uuid4, editable=False, unique=True, db_index = True)
	
	objects = DataSelectionManager()
	
	class Meta:
		ordering = ['owner', '-creation_time']
	
	def __str__(self):
		return '%s on %s' % (self.owner, self.creation_time)
	
	@property
	def zip_file_name(self):
		return self.dataset.name.replace(' ', '_') + '.zip'
	
	@property
	def zip_download_url(self):
		return '%s%s' % (settings.HTTP_BASE_URL, reverse('data_selection:data_selection_download_zip', kwargs = {'uuid': self.uuid}))
	
	@property
	def ftp_download_url(self):
		return '%s/%s' % (settings.FTP_BASE_URL, self.uuid)
