from django.contrib import admin

from hmi_magnetogram.models import Matadata
from common.admin import BaseMatadataAdmin

@admin.register(Matadata)
class MatadataAdmin(BaseMatadataAdmin):
	pass



