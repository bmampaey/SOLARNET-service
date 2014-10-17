from django.conf.urls import patterns, url, include

from wizard import views

urlpatterns = patterns('',
#	url(r'^$', views.index, name='index'),
#	url(r'^login$', views.login, name='login'),
#	url(r'^logout', 'django.contrib.auth.views.logout', name='logout'),
	url(r'^search_dataset$', views.search_dataset, name='search_dataset'),
	url(r'^search/(?P<dataset_name>\w+)$', views.search_data, name='search_data'),
	url(r'^download/(?P<dataset_name>\w+)/(?P<data_id>\d+)$', views.download_data, name='download_data'),
)
