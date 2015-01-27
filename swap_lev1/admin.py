from django.contrib import admin

from swap_lev1.models import Keyword, Tag
from common.admin import KeywordAdmin

admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Tag)

