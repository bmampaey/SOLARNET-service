from django.db import models

__all__ = ['Characteristic']

class Characteristic(models.Model):
	'''Model to define the characteristics of a dataset'''
	name = models.CharField(primary_key = True, max_length = 30)
	
	def __str__(self):
		return self.name
