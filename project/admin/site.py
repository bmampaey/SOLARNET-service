from functools import partial
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from tastypie.admin import ApiKeyInline

# Customize the AdminSite to set adhoc titles and templates
class AdminSite(admin.AdminSite):
	site_header = 'SVO administration interface'
	site_title = 'SVO admin'
	index_title = 'SVO admin'
	site_url = None
	password_change_template = 'admin/password_change.html'
	password_change_done_template = 'admin/password_change_done.html'

site = AdminSite(name='admin')

# Add the Tastypie API key inline
class TastypieUserAdmin(UserAdmin):
	inlines = UserAdmin.inlines + [ApiKeyInline]

site.register(User, TastypieUserAdmin)
site.register(Group, GroupAdmin)

# Redefine the register decorator for our SVO admin site
register = partial(admin.register, site=site)
