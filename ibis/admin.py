
from django.contrib import admin

from .models import Metadata
from dataset.admin import BaseMetadataAdmin

@admin.register(Metadata)
class MetadataAdmin(BaseMetadataAdmin):
	pass
