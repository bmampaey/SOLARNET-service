from django.conf.urls import include, url
from django.contrib import admin

from router import router

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include(router.urls)),
	url(r'^dataset/', include('dataset.urls')),
]
