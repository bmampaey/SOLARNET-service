from django.contrib import admin

from themis.models import Metadata
from common.admin import BaseMetadataAdmin

@admin.register(Metadata)
class MetadataAdmin(BaseMetadataAdmin):
	pass


