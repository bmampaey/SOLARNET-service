from api import svo_api
from .resources import BaseMetadataTestResource

# Register the metadata tests resources
svo_api.register(BaseMetadataTestResource())

app_name = 'metadata'
urlpatterns = []
