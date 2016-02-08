from django.contrib import admin
from aia_lev1.models import Metadata
from dataset.admin import BaseMetadataAdmin

@admin.register(Metadata)
class MetadataAdmin(BaseMetadataAdmin):
	list_filter = BaseMetadataAdmin.list_filter + ["wavelnth"]
	list_display = BaseMetadataAdmin.list_display + ["wavelnth"]
