from django.contrib import admin

from eit.models import Keyword, Tag, MetaData
from common.admin import KeywordAdmin, MetaDataAdmin

admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Tag)

class EitMetaDataAdmin(MetaDataAdmin):
	list_filter = MetaDataAdmin.list_filter + ["wavelnth"]
	list_display = MetaDataAdmin.list_display + ["wavelnth"]

admin.site.register(MetaData, EitMetaDataAdmin)
