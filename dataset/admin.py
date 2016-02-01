from django.contrib import admin
from django.contrib.auth.models import Group
from django import forms
from django.contrib.contenttypes.models import ContentType

from dataset.models import Telescope, Instrument, Characteristic, Dataset, Keyword

class ContentTypeChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s" % (obj.app_label, obj.model)

class DatasetAdminForm(forms.ModelForm):
	'''Form for the admin class for the Dataset model'''
	# Display app label via the ContentTypeChoiceField, and limit to model Metadata (must be in lowcase as it is saved in lowcase)
	_metadata_model = ContentTypeChoiceField(queryset=ContentType.objects.filter(model='metadata')) 
	class Meta:
		model = Dataset
		fields = '__all__'

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
				group = Group.objects.get(name=obj.name)
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
			return queryset.filter(name__in=groups)


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


