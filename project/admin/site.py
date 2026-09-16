from functools import partial

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils.html import format_html, format_html_join
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
	inlines = [*UserAdmin.inlines, ApiKeyInline]
	readonly_fields = UserAdmin.readonly_fields + ('data_selections',)
	fieldsets = UserAdmin.fieldsets + (('Data Selections', {'fields': ('data_selections',)}),)

	def data_selections(self, obj):
		selections = obj.data_selections.all()
		if not selections:
			return 'No data selections'
		return format_html(
			'<ul>{}</ul>',
			format_html_join(
				'\n',
				'<li><a href="{}">{} }</a></li>',
				((reverse('admin:data_selection_dataselection_change', args=[ds.pk]), ds.dataset, ds.uuid) for ds in selections),
			),
		)

	data_selections.short_description = 'Data selections'


class CustomGroupAdmin(GroupAdmin):
	readonly_fields = ['user_list']

	def user_list(self, obj):
		users = obj.user_set.all()
		if not users:
			return 'No users'
		return format_html(
			'<ul>{}</ul>',
			format_html_join(
				'\n',
				'<li><a href="{}">{}</a></li>',
				(
					(
						reverse('admin:auth_user_change', args=[u.pk]),
						u.email,
					)
					for u in users
				),
			),
		)

	user_list.short_description = 'Users'


site.register(User, TastypieUserAdmin)
site.register(Group, CustomGroupAdmin)

# Redefine the register decorator for our SVO admin site
register = partial(admin.register, site=site)
