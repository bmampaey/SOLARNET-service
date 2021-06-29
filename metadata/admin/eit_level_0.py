# Generated by command write_metadata_files version 1
from django.contrib import admin

from metadata.models import EitLevel0
from .base_metadata import BaseMetadataAdmin

__all__ = ['EitLevel0Admin']

@admin.register(EitLevel0)
class EitLevel0Admin(BaseMetadataAdmin):
	list_filter = BaseMetadataAdmin.list_filter + ['wavelnth']
	list_display = BaseMetadataAdmin.list_display + ['wavelnth']
