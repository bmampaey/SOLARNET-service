from django.urls import path, include

from api import svo_api
from api.resources import UserResource

# Import metadata.urls to register the metadata resources before importing svo_api
import metadata.urls # pylint: disable=unused-import

# Register the user resource
svo_api.register(UserResource())

# Do not specify an app_name, this would mess up the api URLs resolution

urlpatterns = [
	path('api/', include(svo_api.urls)),
	path('api_doc/', include('tastypie_swagger.urls'), kwargs={'tastypie_api_module': svo_api, 'namespace': 'tastypie_swagger', 'version': '2'}),
]
