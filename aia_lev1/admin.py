from django.contrib import admin
from aia_lev1.models import Matadata
from common.admin import BaseMatadataAdmin

@admin.register(Matadata)
class MatadataAdmin(BaseMatadataAdmin):
	list_filter = BaseMatadataAdmin.list_filter + ["wavelnth"]
	list_display = BaseMatadataAdmin.list_display + ["wavelnth"]
