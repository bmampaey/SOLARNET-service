# URLs for test settings

from django.urls import path, include
from django.contrib.staticfiles import views

from project.urls import urlpatterns

urlpatterns += [
	path('', include('metadata.tests.urls')),
	path('static/<path:path>', views.serve, kwargs = {'insecure': True})
]
