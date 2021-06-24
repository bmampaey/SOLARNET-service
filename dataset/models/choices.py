from django.db import models

__all__ = ['KeywordType']

class KeywordType(models.TextChoices):
	'''Possible values for the "type" field of the Keyword model'''
	TEXT = 'text', 'text'
	BOOLEAN = 'boolean', 'boolean'
	INTEGER = 'integer', 'integer'
	REAL = 'real', 'real'
	TIME_ISO_8601 = 'time (ISO 8601)', 'time (ISO 8601)'
	
	@classmethod
	def max_length(cls):
			return max(len(value) for value in cls.values)
