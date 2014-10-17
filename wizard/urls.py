from django.conf.urls import patterns, url, include

from wizard import views

urlpatterns = patterns('',
#	url(r'^$', views.index, name='index'),
#	url(r'^login$', views.login, name='login'),
#	url(r'^logout', 'django.contrib.auth.views.logout', name='logout'),
	url(r'^search_data_set$', views.search_data_set, name='search_data_set'),
	url(r'^search_data_set_form$', views.search_data_set_form, name='search_data_set_form'),
	url(r'^search_data_set_results$', views.search_data_set_results, name='search_data_set_results'),
)
