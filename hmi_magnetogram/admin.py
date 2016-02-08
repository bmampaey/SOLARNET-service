from django.contrib import admin

from hmi_magnetogram.models import Metadata
from dataset.admin import BaseMetadataAdmin

@admin.register(Metadata)
class MetadataAdmin(BaseMetadataAdmin):
	pass



