from django.contrib import admin
from aia_lev1.models import Keyword, Tag, MetaData
from common.admin import KeywordAdmin, MetaDataAdmin

class AiaLev1MetaDataAdmin(MetaDataAdmin):
	list_filter = MetaDataAdmin.list_filter + ["wavelnth"]
	list_display = MetaDataAdmin.list_display + ["wavelnth"]

admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Tag)
admin.site.register(MetaData, AiaLev1MetaDataAdmin)



