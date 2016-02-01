from django.contrib import admin

from eit.models import Metadata
from common.admin import BaseMetadataAdmin

@admin.register(Metadata)
class MetadataAdmin(BaseMetadataAdmin):
	pass


