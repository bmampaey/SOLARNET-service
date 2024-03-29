# Generated by command write_metadata_files version 1
from project import admin
from metadata.models import Rosa
from .base_metadata import BaseMetadataAdmin

__all__ = ['RosaAdmin']

@admin.register(Rosa)
class RosaAdmin(BaseMetadataAdmin):
	list_filter = BaseMetadataAdmin.list_filter + ['channel']
	list_display = BaseMetadataAdmin.list_display + ['wavelnth', 'channel']
