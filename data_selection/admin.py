from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from data_selection.models import DataSelectionGroup, DataSelection

@admin.register(DataSelectionGroup)
class DataSelectionGroupAdmin(admin.ModelAdmin):
	'''Admin class for the DataSelectionGroup model'''
	list_display = ['user', 'name', 'created']
	list_filter = ['user__name']
	readonly_fields = ['data_selections', 'ftp_link']
	
	def data_selections(self, instance):
		table_body = format_html_join('\n', '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>', ((ds.dataset, ds.query_string, ds.number_items, ds.created) for ds in instance.data_selections.all()))
		
		if table_body:
			return (mark_safe('<table>\n')
				+ mark_safe('<thead><tr><th>Dataset</th><th>Query string</th><th># items</th><th>Created</th></tr></thead>\n')
				+ mark_safe('<tbody>\n') + table_body + mark_safe('\n</tbody>')
				+ mark_safe('\n</table>'))
		else:
			return mark_safe('<span>None</span>')
	
	# short_description functions like a model field's verbose_name
	data_selections.short_description = 'Data selections'

@admin.register(DataSelection)
class DataSelectionAdmin(admin.ModelAdmin):
	'''Admin class for the DataSelection model'''
	list_display = ['data_selection_group', 'dataset', 'created']
	list_filter = ['dataset']
	readonly_fields = ['number_items']