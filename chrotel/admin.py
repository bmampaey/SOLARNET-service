from django.contrib import admin

from chrotel.models import Metadata
from common.admin import BaseMetadataAdmin

@admin.register(Metadata)
class MetadataAdmin(BaseMetadataAdmin):
	pass
