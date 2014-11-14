from django.contrib import admin

from hmi_magnetogram.models import Keyword, Tag
from common.admin import KeywordAdmin

admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Tag)

