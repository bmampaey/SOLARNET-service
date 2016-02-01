from django.contrib import admin
from daterange_filter.filter import DateRangeFilter

from common.models import DataLocation, Tag


#class FirstLetterListFilter(admin.SimpleListFilter):
#	title = _('First letter')
#	
#	# Parameter for the filter that will be used in the URL query.
#	parameter_name = 'letter'
#	
#	def lookups(self, request, model_admin):
#		return [
#			('A', 'A'),
#			('B', 'B')
#	    ]
#
#	def queryset(self, request, queryset):
#	    return queryset.filter(name__startswith=self.value())


@admin.register(DataLocation)
class DataLocationAdmin(admin.ModelAdmin):
	'''Admin class for the DataLocation model'''
	pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	'''Admin class for the Tag model'''
	pass

class BaseMatadataAdmin(admin.ModelAdmin):
	'''Admin class for the common options of Matadata models'''
	list_filter = [("date_obs", DateRangeFilter)]
	list_display = ["date_obs"]
