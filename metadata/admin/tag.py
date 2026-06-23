from metadata.models import Tag
from project import admin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	"""Admin class for the Tag model"""

	search_fields = ['name']
