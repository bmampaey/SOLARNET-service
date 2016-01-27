from django.contrib import admin

from themis.models import Keyword, Tag, MetaData
from common.admin import KeywordAdmin, MetaDataAdmin

admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Tag)
admin.site.register(MetaData, MetaDataAdmin)
