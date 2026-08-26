import datetime

from django.db import models

__all__ = ['KeywordType', 'KEYWORD_TYPE_CONVERTERS']


class KeywordType(models.TextChoices):
	"""Possible values for the "type" field of the Keyword model"""

	TEXT = 'text', 'text'
	BOOLEAN = 'boolean', 'boolean'
	INTEGER = 'integer', 'integer'
	REAL = 'real', 'real'
	TIME_ISO_8601 = 'time (ISO 8601)', 'time (ISO 8601)'

	@classmethod
	def max_length(cls):
		return max(len(value) for value in cls.values)


# Functions that convert the text of constant_value to the keyword type
def parse_bool(value):
	try:
		return {'true': True, 'false': False}[value]
	except KeyError:
		raise ValueError(f'{value!r} is not a valid boolean string, only acceptable values are "true" or "false"')


KEYWORD_TYPE_CONVERTERS = {
	KeywordType.TEXT: str,
	KeywordType.BOOLEAN: parse_bool,
	KeywordType.INTEGER: int,
	KeywordType.REAL: float,
	KeywordType.TIME_ISO_8601: datetime.datetime.fromisoformat,
}
