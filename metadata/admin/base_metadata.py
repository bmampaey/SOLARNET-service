from urllib.parse import quote as urlquote

from django.contrib.admin import display, widgets
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html

from dataset.models import DataLocation
from project import admin


class BaseMetadataAdmin(admin.ModelAdmin):
	"""Base admin class for the metadata models"""

	date_hierarchy = 'date_beg'
	list_display = ['oid', 'date_beg']
	list_filter = []
	readonly_fields = ['_data_location_url']
	raw_id_fields = ['data_location']

	@display(description='Data Location Url')
	def _data_location_url(self, obj):
		return format_html('<a href={url}>{text}</a>', url=obj.data_location.file_url, text=obj.data_location.file_url)

	def get_readonly_fields(self, request, obj=None):
		"""Return a list or tuple of field names that will be displayed as read-only"""

		# Allow superuser to change everything
		# Allow regular user to set the oid once but not change it
		if obj is None:
			return super().get_readonly_fields(request, obj)
		else:
			return super().get_readonly_fields(request, obj) + ['oid']

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		# For the data_location, only allow the DataLocation with the same dataset as the metadata
		if db_field.name == 'data_location':
			content_type = ContentType.objects.get_for_model(self.model)
			kwargs['widget'] = DataLocationWidget(
				db_field.remote_field,
				self.admin_site,
				using=kwargs.get('using'),
				url_params={'dataset__id__exact': content_type.dataset.id},
			)
			kwargs['queryset'] = DataLocation.objects.filter(dataset=content_type.dataset)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DataLocationWidget(widgets.ForeignKeyRawIdWidget):
	"""ForeignKeyRawIdWidget that allows overidding the URL params in the popup of the magnifying glass"""

	def __init__(self, rel, admin_site, attrs=None, using=None, url_params=None):
		super().__init__(rel, admin_site, attrs, using)
		self.url_params = url_params

	def url_parameters(self):
		params = super().url_parameters()
		if self.url_params:
			params.update(self.url_params)
		return params
