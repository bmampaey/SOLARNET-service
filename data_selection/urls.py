from django.conf.urls import url

from data_selection.views import DownloadDataSelectionGroupView, DownloadDataSelectionView

urlpatterns = [
	url(r'data_selection_group/download_zip/(?P<pk>[0-9]+)/$', DownloadDataSelectionGroupView.as_view(), name='data_selection_group_download_zip'),
	url(r'data_selection/download_zip/(?P<pk>[0-9]+)/$', DownloadDataSelectionView.as_view(), name='data_selection_download_zip'),
]
