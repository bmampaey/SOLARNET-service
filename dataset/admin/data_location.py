from django.contrib import messages
from django.core.exceptions import ValidationError

from project import admin
from dataset.models import DataLocation, Dataset


@admin.register(DataLocation)
class DataLocationAdmin(admin.ModelAdmin):
	'''Admin class for the DataLocation model'''
	list_display = ['file_url', 'dataset', 'file_size', 'offline']
	list_filter = ['dataset']
	list_select_related = ['dataset']
	search_fields = ['file_url']
	readonly_fields = ['update_time']
	date_hierarchy = 'update_time'
	actions = ['mark_offline', 'mark_online']
	
	def get_readonly_fields(self, request, obj=None):
		'''Return a list or tuple of field names that will be displayed as read-only'''
		
		# Allow superuser to change everything
		if request.user.is_superuser:
			return []
		else:
			return super().get_readonly_fields(request, obj)
	
	def get_queryset(self, request):
		'''Return a QuerySet of all model instances that can be edited by the admin site'''
		
		# Display only the data location of the datasets for which the user belong to theirs user_group
		queryset = super().get_queryset(request)
		if request.user.is_superuser:
			return queryset
		else:
			return queryset.filter(dataset__user_group__in = request.user.groups.all())
	
	def has_change_permission(self, request, obj=None):
		'''Return True if editing obj is permitted, False otherwise. If obj is None, return True or False to indicate whether editing of objects of this type is permitted in general'''
		
		# Allow the user to only change a data location if he is a user of the dataset's user_group
		default_permission = super().has_change_permission(request, obj)
		if request.user.is_superuser or obj is None:
			return default_permission
		else:
			return default_permission and obj.dataset.user_group in request.user.groups.all()
	
	def has_delete_permission(self, request, obj=None):
		'''Return True if deleting obj is permitted, False otherwise. If obj is None, return True or False to indicate whether deleting objects of this type is permitted in general'''
	
		# Allow the user to only delete a data location if he is a user of the dataset's user_group
		default_permission = super().has_delete_permission(request, obj)
		if request.user.is_superuser or obj is None:
			return default_permission
		else:
			return default_permission and obj.dataset.user_group in request.user.groups.all()
		
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		'''Return the formfield for a foreign key field'''
		
		# Allow the user to only add a data location to a datasets if he is a user of that dataset's user_group
		if not request.user.is_superuser and db_field.name == 'dataset':
			kwargs['queryset'] = Dataset.objects.filter(user_group__in = request.user.groups.all())
		return super().formfield_for_foreignkey(db_field, request, **kwargs)
	
	def get_object(self, request, object_id, from_field=None):
		'''Return an instance matching the field and value provided'''
		
		# Redefine get_object because the default one uses get_queryset where we filter out the instances that are not accessible by the request user
		# as a consequence has_change_permission and has_delete_permission will receive None instead of an instance when trying to change/delete an object that is not accessible by the request user
		# instead just use the _default_manager of the model
		field = self.model._meta.pk if from_field is None else self.model._meta.get_field(from_field)
		try:
				object_id = field.to_python(object_id)
				queryset = self.model._default_manager.get_queryset()
				return queryset.get(**{field.name: object_id})
		except (self.model.DoesNotExist, ValidationError, ValueError):
					return None
	
	@admin.action(description='Mark selected as offline')
	def mark_offline(self, request, queryset):
		update_count = queryset.update(offline=True)
		self.message_user(request, '%d data locations were successfully marked as offline' % update_count, messages.SUCCESS)
	
	@admin.action(description='Mark selected as online')
	def mark_online(self, request, queryset):
		update_count = queryset.update(offline=False)
		self.message_user(request, '%d data locations were successfully marked as online' % update_count, messages.SUCCESS)
