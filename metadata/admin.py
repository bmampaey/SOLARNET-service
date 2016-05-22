from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe

from daterange_filter.filter import DateRangeFilter

from metadata.models import Tag, AiaLev1, Chrotel, Eit, HmiMagnetogram, SwapLev1, Themis, Xrt
from metadata.forms import AddTagForm

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
	list_filter = [('date_beg', DateRangeFilter)]
	list_display = ['oid', 'date_beg']
	readonly_fields = ['data_location']
	action_form = AddTagForm
	actions = ['add_tags']
	
	def add_tags(self, request, queryset):
		form = AddTagForm(request.POST)
		# action choices are added dynamically in django admin
		form.fields['action'].choices = self.get_action_choices(request)
		
		if form.is_valid():
			tags = form.cleaned_data['tags']
			for metadata in queryset:
				metadata.tags.add(*tags)
			self.message_user(request, "Successfully tagged %s metadata." % queryset.count())
		else:
			self.message_user(request, mark_safe("Error tagging metadata: %s." % form.errors), level=messages.ERROR)
	add_tags.short_description = u'Add tags to selected metadata'

@admin.register(AiaLev1)
class AiaLev1Admin(BaseMetadataAdmin):
	list_filter = BaseMetadataAdmin.list_filter + ["wavelnth"]
	list_display = BaseMetadataAdmin.list_display + ["wavelnth"]

@admin.register(Chrotel)
class ChrotelAdmin(BaseMetadataAdmin):
	list_filter = BaseMetadataAdmin.list_filter + ["wavelnth"]
	list_display = BaseMetadataAdmin.list_display + ["wavelnth"]

@admin.register(Eit)
class EitAdmin(BaseMetadataAdmin):
	list_filter = BaseMetadataAdmin.list_filter + ["wavelnth"]
	list_display = BaseMetadataAdmin.list_display + ["wavelnth"]

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
	list_filter = BaseMetadataAdmin.list_filter + ["target"]
	list_display = BaseMetadataAdmin.list_display + ["target", "noaa_num"]