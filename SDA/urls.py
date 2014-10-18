from django.conf.urls import patterns, include, url
from django.contrib import admin
from SDA.api import v1_api

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include(v1_api.urls)),
	url(r'^wizard/', include('wizard.urls')),
	url(r'^wizard/', include('dataset.urls')),
)
