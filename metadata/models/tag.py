from django.db import models

__all__ = ['Tag']

class Tag(models.Model):
	'''Metadata tag model'''
	name = models.CharField(primary_key=True, max_length=30, blank=False, null=False)
	
	def __str__(self):
		return self.name
