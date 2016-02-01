from django.contrib import admin

from swap_lev1.models import Matadata
from common.admin import BaseMatadataAdmin

@admin.register(Matadata)
class MatadataAdmin(BaseMatadataAdmin):
	pass



