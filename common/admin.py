from django.contrib import admin
from daterange_filter.filter import DateRangeFilter

class KeywordAdmin(admin.ModelAdmin):
	list_display = ("name", "python_type", "unit", "description")
	
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return self.readonly_fields + ("db_column",)
		return self.readonly_fields


class MetaDataAdmin(admin.ModelAdmin):
	list_filter = [("date_obs", DateRangeFilter)]
	list_display = ["date_obs"]
