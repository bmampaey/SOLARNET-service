from django.contrib import admin

class KeywordAdmin(admin.ModelAdmin):
	list_display = ("name", "python_type", "unit", "description")
	
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return self.readonly_fields + ("column",)
		return self.readonly_fields
