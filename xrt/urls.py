from django.conf.urls import patterns, url, include

from xrt import views

urlpatterns = patterns('',
	url(r'^search_data_form$', views.SearchDataForm.as_view(), name='search_data_form'),
	url(r'^search_data_results$', views.SearchDataResults.as_view(), name='search_data_results'),
	url(r'^download_data/(?P<data_id>\d+)$', views.DownloadData.as_view(), name='download_data'),
)

