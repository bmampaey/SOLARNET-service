from django.contrib import admin

from chrotel.models import Keyword, Tag, MetaData
from common.admin import KeywordAdmin, MetaDataAdmin

admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Tag)

class ChrotelMetaDataAdmin(MetaDataAdmin):
	list_filter = MetaDataAdmin.list_filter
	list_display = MetaDataAdmin.list_display

admin.site.register(MetaData, ChrotelMetaDataAdmin)
