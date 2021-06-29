from django.contrib import admin

from dataset.models import Telescope


@admin.register(Telescope)
class TelescopeAdmin(admin.ModelAdmin):
	'''Admin class for the Telescope model'''
	pass
