from django.urls import path

from api import svo_api
from data_selection.resources import DataSelectionResource
from data_selection.views import DataSelectionDownloadZipView

# Register the data_selection resources
svo_api.register(DataSelectionResource())

app_name = 'data_selection'

urlpatterns = [
	path('download_zip/<uuid:uuid>/', DataSelectionDownloadZipView.as_view(), name='data_selection_download_zip'),
]
