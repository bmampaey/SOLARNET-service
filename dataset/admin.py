from django.contrib import admin

from dataset.models import DataSet
# Register your models here.

class DataSetAdmin(admin.ModelAdmin):
	list_display = ("name", "instrument", "contact")
	
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return self.readonly_fields + ("name",)
		return self.readonly_fields

admin.site.register(DataSet, DataSetAdmin)

