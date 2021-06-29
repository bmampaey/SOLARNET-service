from django.urls import re_path
from django.contrib.staticfiles import views

# Import metadata.tests.urls to register the metadata test resources before importing the base urls
import metadata.tests.urls # pylint: disable=unused-import
from .urls import urlpatterns

# URLs for the testing
urlpatterns += [
	re_path(r'^static/(?P<path>.*)$', views.serve, kwargs = {'insecure': True})
]
