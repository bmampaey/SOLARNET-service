# Generated by command write_metadata_files version 1
from project import admin
from metadata.models import GaiaDem
from .base_metadata import BaseMetadataAdmin

__all__ = ['GaiaDemAdmin']

@admin.register(GaiaDem)
class GaiaDemAdmin(BaseMetadataAdmin):
	pass