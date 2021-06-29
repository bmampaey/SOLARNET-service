from django.contrib import admin

from dataset.models import Characteristic


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
	'''Admin class for the Characteristic model'''
	pass
