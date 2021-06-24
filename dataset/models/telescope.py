from django.db import models

__all__ = ['Telescope']

class Telescope(models.Model):
	'''Model for the description of a telescope'''
	name = models.CharField(primary_key = True, max_length = 30)
	description = models.TextField(help_text = 'Telescope description', blank = True, null = True)
	
	def __str__(self):
		return self.name
