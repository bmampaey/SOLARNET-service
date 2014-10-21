from django.conf.urls import patterns, url, include

from wizard import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
#	url(r'^login$', views.login, name='login'),
#	url(r'^logout', 'django.contrib.auth.views.logout', name='logout'),
)
