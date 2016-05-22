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
	
	def has_add_permission(self, request):
		return request.user.is_superuser
	
	def has_change_permission(self, request, obj=None):
		# Allow to change only datasets for wich the user has access to
		if request.user.is_superuser:
			return True
		elif obj is not None:
			try:
				group = Group.objects.get(name=obj.id)
			except Group.DoesNotExist:
				return False
			else:
				return group in request.user.groups.all()
		else:
			return True
	
	def has_delete_permission(self, request, obj=None):
		return request.user.is_superuser
	
	def get_queryset(self, request):
		# Display only datasets for wich the user has access to
		queryset = super(DatasetAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return queryset
		else:
			groups = [group.name for group in request.user.groups.all()]
			return queryset.filter(id__in=groups)

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
	'''Admin class for the Keyword model'''
	list_display = ["name", "python_type", "unit", "description"]
	list_filter = ["dataset__name"]
	
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return self.readonly_fields + ("db_column",)
		return self.readonly_fields

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


