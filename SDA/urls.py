from django.conf.urls import include, url
from django.contrib import admin
from SDA.api import api

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^dataset/', include('dataset.urls')),
	url(r'^data_selection/', include('data_selection.urls')),
	url(r'^api/', include(api.urls)),
	url(r'^api/doc/', include(('tastypie_swagger.urls', 'api_doc')),kwargs={"tastypie_api_module": api, 'namespace': 'api_doc'}),
]
