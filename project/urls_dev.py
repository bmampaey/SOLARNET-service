from django.urls import path, include

from .urls import urlpatterns

# URLs for the development server
urlpatterns += [
	path('__debug__/', include('debug_toolbar.toolbar'))
]
