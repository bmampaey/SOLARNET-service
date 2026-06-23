# URLs for test settings

from django.contrib.staticfiles import views
from django.urls import include, path

from project.urls import urlpatterns

urlpatterns += [
	path('', include('metadata.tests.urls')),
	path('static/<path:path>', views.serve, kwargs={'insecure': True}),
]
