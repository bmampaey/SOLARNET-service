# Generated by command write_metadata_files version 1
from django.contrib import admin

from metadata.models import Themis
from .base_metadata import BaseMetadataAdmin

__all__ = ['ThemisAdmin']

@admin.register(Themis)
class ThemisAdmin(BaseMetadataAdmin):
	pass
