from django.contrib import admin

from xrt.models import Metadata
from common.admin import BaseMetadataAdmin

@admin.register(Metadata)
class MetadataAdmin(BaseMetadataAdmin):
	pass

