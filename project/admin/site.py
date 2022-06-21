from functools import partial
from django.contrib import admin


# Customize the AdminSite to set adhoc titles and templates
class AdminSite(admin.AdminSite):
	site_header = 'SVO administration interface'
	site_title = 'SVO admin'
	index_title = 'SVO admin'
	site_url = None
	password_change_template = 'admin/password_change.html'
	password_change_done_template = 'admin/password_change_done.html'

site = AdminSite(name='admin')

register = partial(admin.register, site=site)
