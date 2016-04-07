from django.contrib import admin
from web_account.models import User


class FirstLetterListFilter(admin.SimpleListFilter):
	title = 'First letter'
	
	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'username'
	
	def lookups(self, request, model_admin):
		'''List the first letter of existing users'''
		qs = model_admin.get_queryset(request)
		return set((obj.username[0].upper(), obj.username[0].upper()) for obj in qs)

	def queryset(self, request, queryset):
		if self.value() is not None:
			return queryset.filter(username__istartswith=self.value())
		else:
			return queryset

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	'''Admin class for the web account User model'''
	list_display = ['username', 'email', 'last_login']
	list_filter = [FirstLetterListFilter]
	
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return self.readonly_fields + ('email',)
		return self.readonly_fields
