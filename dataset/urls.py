from django.conf.urls import url
from dataset import views

urlpatterns = [
	url(r'data/(?P<dataset_id>[a-z][_a-z0-9]*)/(?P<metadata_oid>\w+)/$', views.Data.as_view(), name='data'),
	url(r'thumbnail/(?P<dataset_id>[a-z][_a-z0-9]*)/(?P<metadata_oid>\w+)/$', views.Thumbnail.as_view(), name='thumbnail'),
]
