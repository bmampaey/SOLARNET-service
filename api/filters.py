from django.db import models
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS

__all__ = ['FILTERS', 'FIELD_FILTERS', 'get_relational_filters']


class FILTERS:
	"""Define the possible filter lookup per ressource field category"""

	# Select among 'exact', 'iexact', 'contains', 'icontains', 'in', 'gt', 'gte', 'lt', 'lte',
	# 'startswith', 'istartswith', 'endswith', 'iendswith', 'range',
	# 'date', 'year', 'iso_year', 'month', 'day', 'week', 'week_day', 'iso_week_day', 'quarter', 'time', 'hour', 'minute', 'second',
	# 'isnull', 'regex', 'iregex'
	BOOLEAN = ['exact', 'isnull']
	NUMERIC = ['exact', 'in', 'gt', 'gte', 'lt', 'lte', 'range', 'isnull']
	TEXT = [
		'exact',
		'iexact',
		'contains',
		'icontains',
		'in',
		'startswith',
		'istartswith',
		'endswith',
		'iendswith',
		'isnull',
		'regex',
		'iregex',
	]
	# Tastypie does not support datetime casting filters like __hour, __date, etc.
	DATETIME = ['exact', 'in', 'gt', 'gte', 'lt', 'lte', 'range', 'isnull']
	COMPLEX_SEARCH_EXPRESSION = ['complex-search-expression']


FIELD_FILTERS = {
	fields.BooleanField: FILTERS.BOOLEAN,
	fields.CharField: FILTERS.TEXT,
	fields.DateField: FILTERS.DATETIME,
	fields.DateTimeField: FILTERS.DATETIME,
	fields.DecimalField: FILTERS.NUMERIC,
	fields.FloatField: FILTERS.NUMERIC,
	fields.IntegerField: FILTERS.NUMERIC,
	fields.TimeField: FILTERS.DATETIME,
}


# For relational filters, Tastypie has defined the constant ALL_WITH_RELATIONS but it shows as 2 in the schema
# To improve the schema readability, we create a list such that when the Tatsypie library does a filter == ALL_WITH_RELATIONS it will return true
# but when use din the schema, it will show the list content
class HackList(list):
	def __eq__(self, other):
		return other == ALL_WITH_RELATIONS or super().__eq__(other)

	def __neq__(self, other):
		return not self.__eq__(other)


# Tastypie only allow the direct comparison on related, so only specify __in
# see https://github.com/django-tastypie/django-tastypie/pull/1619
def get_relational_filters(resource):
	"""Inspect a resource and return the list of filters"""
	return HackList(f'{field}{lookup}' for field, lookups in resource._meta.filtering.items() for lookup in ('', '__in'))
	return HackList(resource._meta.filtering.keys())
