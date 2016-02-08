from django.conf.urls import url, include
from rest_framework import routers

from dataset import views

#DRF url router
router = routers.DefaultRouter()
router.register(r'telescope', views.TelescopeViewSet)
router.register(r'instrument', views.InstrumentViewSet)
router.register(r'data_location', views.DataLocationViewSet)
router.register(r'dataset', views.DatasetViewSet)
router.register(r'characteristic', views.CharacteristicViewSet)
router.register(r'keyword', views.KeywordViewSet)
router.register(r'tag', views.TagViewSet)


urlpatterns = [
	url(r'download_data/(?P<dataset_id>[a-z][_a-z0-9]*)/(?P<metadata_oid>\d+)/$', views.DownloadData.as_view(), name='download_data'),
	url(r'^', include(router.urls)),
]
