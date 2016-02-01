from django.contrib import admin

from swap_lev1.models import Metadata
from common.admin import BaseMetadataAdmin

@admin.register(Metadata)
class MetadataAdmin(BaseMetadataAdmin):
	pass



