from django.contrib import admin
from daterange_filter.filter import DateRangeFilter

from metadata.models import Tag, AiaLev1, Chrotel, Eit, HmiMagnetogram, SwapLev1, Themis, Xrt

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

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	'''Admin class for the Tag model'''
	list_filter = [FirstLetterListFilter]

class BaseMetadataAdmin(admin.ModelAdmin):
	'''Admin class for the common options of Metadata models'''
	list_filter = [('date_beg', DateRangeFilter), 'wavemin']
	list_display = ['oid', 'date_beg', 'wavemin']
	readonly_fields = ['data_location']

@admin.register(AiaLev1)
class AiaLev1Admin(BaseMetadataAdmin):
	list_filter = BaseMetadataAdmin.list_filter + ["wavelnth"]
	list_display = BaseMetadataAdmin.list_display + ["wavelnth"]

@admin.register(Chrotel)
class ChrotelAdmin(BaseMetadataAdmin):
	pass

@admin.register(Eit)
class EitAdmin(BaseMetadataAdmin):
	pass

@admin.register(HmiMagnetogram)
class HmiMagnetogramAdmin(BaseMetadataAdmin):
	pass

@admin.register(SwapLev1)
class SwapLev1Admin(BaseMetadataAdmin):
	pass

@admin.register(Themis)
class ThemisAdmin(BaseMetadataAdmin):
	pass

@admin.register(Xrt)
class XrtAdmin(BaseMetadataAdmin):
	pass