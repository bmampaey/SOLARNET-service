# Generated by command write_metadata_files version 1
from project import admin
from metadata.models import EuiLevel2
from .base_metadata import BaseMetadataAdmin

__all__ = ['EuiLevel2Admin']

@admin.register(EuiLevel2)
class EuiLevel2Admin(BaseMetadataAdmin):
	pass
