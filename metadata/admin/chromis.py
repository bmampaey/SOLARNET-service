# Generated by command write_metadata_files version 1
from project import admin
from metadata.models import Chromis
from .base_metadata import BaseMetadataAdmin

__all__ = ['ChromisAdmin']

@admin.register(Chromis)
class ChromisAdmin(BaseMetadataAdmin):
	pass
