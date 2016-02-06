from django.conf.urls import url

from dataset import views

urlpatterns = [
	url(r'download_data/(?P<dataset_id>[a-z][_a-z0-9]*)/(?P<metadata_oid>\d+)/$', views.DownloadData.as_view(), name='download_data'),
]
