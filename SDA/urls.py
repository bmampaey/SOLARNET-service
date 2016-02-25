from django.conf.urls import include, url
from django.contrib import admin
from SDA.api import v1_api

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^dataset/', include('dataset.urls')),
	url(r'^api/', include(v1_api.urls)),
]
