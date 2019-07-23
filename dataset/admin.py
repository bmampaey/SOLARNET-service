from django.contrib import admin
from django.contrib.auth.models import Group

from dataset.models import Telescope, Instrument, Characteristic, Dataset, Keyword, DataLocation
from dataset.forms import DatasetAdminForm


# For this class to work there must be for each dataset a group with the same name
@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
	'''Admin class for the Dataset model'''
	form = DatasetAdminForm
	list_display = ["name", "telescope", "instrument", "contact"]
	filter_horizontal = ["characteristics"]
	
	def get_readonly_fields(self, request, obj=None):
		# Do not allow to change the name of the dataset
		if obj:
			return self.readonly_fields + ("id",)
		return self.readonly_fields
	
	def get_queryset(self, request):
		# Display only datasets for wich the user has access to
		queryset = super(DatasetAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return queryset
		return queryset.filter(id__in = request.user.groups.values_list('name', flat = True))


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
	'''Admin class for the Keyword model'''
	list_display = ["name", "python_type", "unit", "description"]
	list_filter = ["dataset__name"]
	
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return self.readonly_fields + ("db_column",)
		return self.readonly_fields
	
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if not request.user.is_superuser and db_field.name == 'dataset':
			kwargs['queryset'] = Dataset.objects.filter(id__in = request.user.groups.values_list('name', flat = True))
		return super(KeywordAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
	
	def get_queryset(self, request):
		queryset = super(KeywordAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return queryset
		return queryset.filter(dataset_id__in = request.user.groups.values_list('name', flat = True))

@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
	'''Admin class for the Characteristic model'''
	pass

@admin.register(Telescope)
class TelescopeAdmin(admin.ModelAdmin):
	'''Admin class for the Telescope model'''
	pass

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
	'''Admin class for the Instrument model'''
	pass


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
			return queryset.filter(**{'%s__isnull' % self.value() : False})
		else:
			return queryset


@admin.register(DataLocation)
class DataLocationAdmin(admin.ModelAdmin):
	'''Admin class for the DataLocation model'''
	list_filter = [DatasetListFilter]
