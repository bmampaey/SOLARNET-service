from django.contrib import admin
from SDA.admin import KeywordAdmin

# Register your models here.

from eit.models import Keyword

admin.site.register(Keyword, KeywordAdmin)

