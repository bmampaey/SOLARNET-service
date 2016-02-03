from django.contrib import admin
from daterange_filter.filter import DateRangeFilter

from common.models import DataLocation, Tag
from dataset.models import Dataset


class FirstLetterListFilter(admin.SimpleListFilter):
	title = 'First letter'
	
	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'starts_with'
	
	def lookups(self, request, model_admin):
		'''List the first letter of existing tags'''
		qs = model_admin.get_queryset(request)
		return set((obj.name[0].upper(), obj.name[0].upper()) for obj in qs)

	def queryset(self, request, queryset):
		if self.value() is not None:
			return queryset.filter(name__istartswith=self.value())
		else:
			return queryset


class DatasetListFilter(admin.SimpleListFilter):
	title = 'Dataset'
	
	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'dataset'
	
	def lookups(self, request, model_admin):
		'''List the existing datasets'''
		return [(dataset.id, dataset.name) for dataset in Dataset.objects.all()]

	def queryset(self, request, queryset):
		# TODO check that it is correct
		if self.value() is not None:
			return queryset.filter(**{'%s_metadata__isnull' % self.value() : False})
		else:
			return queryset


@admin.register(DataLocation)
class DataLocationAdmin(admin.ModelAdmin):
	'''Admin class for the DataLocation model'''
	list_filter = [DatasetListFilter]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	'''Admin class for the Tag model'''
	list_filter = [FirstLetterListFilter]

class BaseMetadataAdmin(admin.ModelAdmin):
	'''Admin class for the common options of Metadata models'''
	list_filter = [('date_beg', DateRangeFilter), 'wavemin']
	list_display = ['date_beg', 'wavemin']
