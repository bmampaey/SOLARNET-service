from django.contrib import admin

from eit.models import Keyword, Tag
from common.admin import KeywordAdmin

admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Tag)

