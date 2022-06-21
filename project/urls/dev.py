# URLs for dev settings
from django.urls import path, include

from project.urls import urlpatterns

urlpatterns += [
	path('__debug__/', include('debug_toolbar.urls'))
]
