from django.contrib import admin

from themis.models import Matadata
from common.admin import BaseMatadataAdmin

@admin.register(Matadata)
class MatadataAdmin(BaseMatadataAdmin):
	pass


