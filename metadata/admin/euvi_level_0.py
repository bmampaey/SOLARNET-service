# Generated by command write_metadata_files version 1
from django.contrib import admin

from metadata.models import EuviLevel0
from .base_metadata import BaseMetadataAdmin

__all__ = ['EuviLevel0Admin']

@admin.register(EuviLevel0)
class EuviLevel0Admin(BaseMetadataAdmin):
	pass