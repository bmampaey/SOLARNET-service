from django.contrib import admin
from django.contrib.auth.models import Group
from dataset.models import Dataset
# Register your models here.

class DatasetAdmin(admin.ModelAdmin):
	list_display = ("name", "instrument", "contact")
	
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return self.readonly_fields + ("name",)
		return self.readonly_fields
	
	def has_add_permission(self, request):
		return request.user.is_superuser
	
	def has_change_permission(self, request, obj=None):
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
		queryset = super(DatasetAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return queryset
		else:
			groups = [group.name for group in request.user.groups.all()]
			return queryset.filter(name__in=groups)

admin.site.register(Dataset, DatasetAdmin)

