from django.db import models
from .validators import valid_file_path

__all__ = ['DataLocation']

class DataLocationManager(models.Manager):
	'''Manager that optimize the queries by selecting the foreign objects'''
	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.select_related('dataset')
		return queryset

class DataLocation(models.Model):
	'''Model to define a data file of a dataset'''
	dataset = models.ForeignKey('Dataset', on_delete = models.CASCADE, related_name = 'data_locations')
	file_url = models.URLField('File URL', max_length = 2000, help_text = 'URL of the data file at the remote site')
	file_size = models.PositiveBigIntegerField(help_text = 'Size of the data file in bytes')
	file_path = models.TextField(help_text = r'File name or relative path of the data file, use / as the path separator and avoid the characters \:*?"\'<>|\r\n\0', db_index = True, validators = [valid_file_path])
	thumbnail_url = models.URLField('Thumbnail URL', max_length = 2000, help_text = 'URL of the thumbnail image at the remote site', blank = True, null = True)
	update_time = models.DateTimeField(auto_now = True, help_text = 'Date of last update')
	offline = models.BooleanField(default = False, help_text = 'The data is not available for download') # , choices = [(True, 'true'), (False, 'false')]
	
	objects = DataLocationManager()
	
	class Meta:
		unique_together = [('dataset', 'file_url'), ('dataset', 'file_path')]
	
	def __str__(self):
		return self.file_url
