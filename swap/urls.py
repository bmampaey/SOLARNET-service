from django.conf.urls import patterns, url, include

from swap import views

urlpatterns = patterns('',
	url(r'^search_data_form$', views.search_data_form, name='search_data_form'),
	url(r'^search_data_results$', views.search_data_results, name='search_data_results'),
	url(r'^download_data/(?P<data_id>\d+)$', views.download_data, name='download_data'),
)

