from django.conf.urls import patterns, include, url
from django.contrib import admin
from SDA.api import v1_api


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include(v1_api.urls)),
#	url(r'^dataset/', include('dataset.urls')),
#	url(r'^eit/', include('eit.urls', namespace='eit')),
#	url(r'^swap_lev1/', include('swap_lev1.urls', namespace='swap_lev1')),
#	url(r'^aia_lev1/', include('aia_lev1.urls', namespace='aia_lev1')),
#	url(r'^hmi_magnetogram/', include('hmi_magnetogram.urls', namespace='hmi_magnetogram')),
#	url(r'^themis/', include('themis.urls', namespace='themis')),
#	url(r'^wizard/', include('wizard.urls')),
]
