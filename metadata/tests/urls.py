from django.urls import re_path, include

from api import svo_api
from .resources import BaseMetadataTestResource

# Register the metadata tests resources
base_metadata_test_resource = BaseMetadataTestResource()
svo_api.register(base_metadata_test_resource)
urlpatterns = [
	re_path(r'^(?P<api_name>%s)/' % svo_api.api_name, include(base_metadata_test_resource.urls)),
]
