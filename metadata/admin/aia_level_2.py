# Generated by command write_metadata_files version 1
from project import admin
from metadata.models import AiaLevel2
from .base_metadata import BaseMetadataAdmin

__all__ = ['AiaLevel2Admin']

@admin.register(AiaLevel2)
class AiaLevel2Admin(BaseMetadataAdmin):
	pass
