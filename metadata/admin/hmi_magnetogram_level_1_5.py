# Generated by command write_metadata_files version 1
from project import admin
from metadata.models import HmiMagnetogramLevel15
from .base_metadata import BaseMetadataAdmin

__all__ = ['HmiMagnetogramLevel15Admin']

@admin.register(HmiMagnetogramLevel15)
class HmiMagnetogramLevel15Admin(BaseMetadataAdmin):
	pass
