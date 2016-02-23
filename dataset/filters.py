from rest_framework.filters import DjangoFilterBackend
from django.db import models
from django.db.models.sql.constants import QUERY_TERMS


class MetadataFilterBackend(DjangoFilterBackend):
	'''A filter backend for Metadata that allows filtering on all fields but data_location.'''
	
	def get_filter_class(self, view, queryset=None):
		'''Return the django-filters `FilterSet` used to filter the queryset.'''
		filter_class = getattr(view, 'filter_class', None)
		filter_fields = getattr(view, 'filter_fields', None)
		
		# If filters have been set explicitly, use it
		if filter_class or filter_fields:
			return super(MetadataFilterBackend, self).get_filter_class(self, view, queryset)
		
		# Else create a Filterset for all regular fields
		field_names = [field.name for field in queryset.model._meta.get_fields() if not field.is_relation and not field.auto_created]
		filter_fields = dict((name, QUERY_TERMS) for name in field_names)
		
		class MetadataFilterSet(self.default_filter_set):
			class Meta:
				model = queryset.model
				fields = filter_fields
		return MetadataFilterSet
	