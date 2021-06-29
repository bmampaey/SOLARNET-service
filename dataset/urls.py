from django.urls import path

from api import svo_api
from dataset.resources import DatasetResource, CharacteristicResource, TelescopeResource, InstrumentResource, KeywordResource, DataLocationResource
from dataset.views import DataView, ThumbnailView

# Register the dataset resources
svo_api.register(DatasetResource())
svo_api.register(CharacteristicResource())
svo_api.register(TelescopeResource())
svo_api.register(InstrumentResource())
svo_api.register(KeywordResource())
svo_api.register(DataLocationResource())


app_name = 'dataset'
urlpatterns = [
	path('data/<str:dataset_name>/<str:metadata_oid>/', DataView.as_view(), name='data'),
	path('thumbnail/<str:dataset_name>/<str:metadata_oid>/', ThumbnailView.as_view(), name='thumbnail'),
]
