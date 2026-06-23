from data_selection.models import DataSelection
from project import admin


@admin.register(DataSelection)
class DataSelectionAdmin(admin.ModelAdmin):
	"""Admin class for the DataSelection model"""

	list_display = ['__str__', 'dataset']
	list_filter = ['dataset']
	readonly_fields = ['creation_time', 'uuid']
	date_hierarchy = 'creation_time'
