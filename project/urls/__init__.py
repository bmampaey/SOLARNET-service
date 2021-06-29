from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('admin/', admin.site.urls),
	path('data_selection/', include('data_selection.urls', namespace='data_selection')),
	path('', include('dataset.urls', namespace='dataset')),
	path('', include('api.urls')),
]
