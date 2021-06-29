from django.contrib import admin

from metadata.models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	'''Admin class for the Tag model'''
	search_fields = ['name']
