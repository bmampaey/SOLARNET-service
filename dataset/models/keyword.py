from django.db import models

from .validators import valid_keyword_name
from .choices import KeywordType

__all__ = ['Keyword']


class KeywordManager(models.Manager):
	'''Manager that optimize the queries by selecting the foreign objects'''
	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.select_related('dataset')
		return queryset

class Keyword(models.Model):
	'''Model to define a metadata keyword of a dataset'''
	
	dataset = models.ForeignKey('Dataset', on_delete = models.CASCADE, related_name = 'keywords')
	name = models.CharField(max_length = 200, help_text = 'Name of the corresponding field in the metadata model, can contain only letters, digits and underscore', validators = [valid_keyword_name])
	verbose_name = models.CharField(max_length = 200, help_text = 'Verbose name of the keyword, can contain any unicode character')
	type = models.CharField(max_length = KeywordType.max_length(), default = KeywordType.TEXT, choices = KeywordType.choices, help_text = 'Python type of the keyword')
	unit = models.CharField(max_length = 30, help_text = 'Physical unit (SI compliant) of the keyword', blank = True, null = True)
	description = models.TextField(help_text = 'Full description of the keyword', blank = True, null = True)
	
	objects = KeywordManager()
	
	class Meta:
		ordering = ['dataset', 'name']
		unique_together = [('dataset', 'name'), ('dataset', 'verbose_name')]
		
	def __str__(self):
		return self.verbose_name
