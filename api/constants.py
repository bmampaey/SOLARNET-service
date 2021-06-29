from django.db import models
from tastypie.constants import ALL_WITH_RELATIONS

__all__ = ['FILTERS', 'FIELD_FILTERS']


# HACK: when defining a filter with ALL_WITH_RELATIONS, it shows as "2" in the schema
# so override it with a __str__ to display a more human friendly message in the schema
# but still evaluates as ALL_WITH_RELATIONS. e.g RelationalFilters(ALL_WITH_RELATIONS) == ALL_WITH_RELATIONS
class RelationalFilters(int):
	def __str__(self):
		return 'relational filters'


class FILTERS:
	'''Define the possible applicable filters per ressource field category'''
	# Select among 'exact', 'iexact', 'contains', 'icontains', 'in', 'gt', 'gte', 'lt', 'lte', 'startswith', 'istartswith', 'endswith', 'iendswith', 'range', 'date', 'year', 'iso_year', 'month', 'day', 'week', 'week_day', 'iso_week_day', 'quarter', 'time', 'hour', 'minute', 'second', 'isnull', 'regex', 'iregex'
	BOOLEAN = ['exact', 'isnull']
	NUMERIC = ['exact', 'in', 'gt', 'gte', 'lt', 'lte', 'range', 'isnull']
	TEXT = ['exact', 'iexact', 'contains', 'icontains', 'in', 'startswith', 'istartswith', 'endswith', 'iendswith', 'isnull', 'regex', 'iregex']
	# Tastypie does not support datetime casting filters like __hour, __date, etc.
	DATETIME = ['exact', 'in', 'gt', 'gte', 'lt', 'lte', 'range', 'isnull']
	RELATIONAL = RelationalFilters(ALL_WITH_RELATIONS)
	COMPLEX_SEARCH_EXPRESSION = 'complex search expression'

FIELD_FILTERS = {
	models.AutoField: FILTERS.NUMERIC,
	models.BigAutoField: FILTERS.NUMERIC,
	models.BigIntegerField: FILTERS.NUMERIC,
	models.BooleanField: FILTERS.BOOLEAN,
	models.CharField: FILTERS.TEXT,
	models.DateField: FILTERS.DATETIME,
	models.DateTimeField: FILTERS.DATETIME,
	models.DecimalField: FILTERS.NUMERIC,
	models.DurationField: FILTERS.NUMERIC,
	models.EmailField: FILTERS.TEXT,
	models.FilePathField: FILTERS.TEXT,
	models.FloatField: FILTERS.NUMERIC,
	models.IntegerField: FILTERS.NUMERIC,
	models.GenericIPAddressField: FILTERS.TEXT,
	models.PositiveBigIntegerField: FILTERS.NUMERIC,
	models.PositiveIntegerField: FILTERS.NUMERIC,
	models.PositiveSmallIntegerField: FILTERS.NUMERIC,
	models.SlugField: FILTERS.TEXT,
	models.SmallAutoField: FILTERS.NUMERIC,
	models.SmallIntegerField: FILTERS.NUMERIC,
	models.TextField: FILTERS.TEXT,
	models.TimeField: FILTERS.DATETIME,
	models.URLField: FILTERS.TEXT,
	models.UUIDField: FILTERS.TEXT,
}
