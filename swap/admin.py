from django.contrib import admin
from common.admin import KeywordAdmin

# Register your models here.

from swap.models import Keyword

admin.site.register(Keyword, KeywordAdmin)
