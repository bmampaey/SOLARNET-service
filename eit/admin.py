from django.contrib import admin

from eit.models import Matadata
from common.admin import BaseMatadataAdmin

@admin.register(Matadata)
class MatadataAdmin(BaseMatadataAdmin):
	pass


