from django.contrib import admin

from swap.models import Keyword
from common.admin import KeywordAdmin

admin.site.register(Keyword, KeywordAdmin)

