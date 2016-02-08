from django.contrib import admin

from xrt.models import Metadata
from dataset.admin import BaseMetadataAdmin

@admin.register(Metadata)
class MetadataAdmin(BaseMetadataAdmin):
	pass

