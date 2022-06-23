from django.urls import path, include

# WARNING for some reason auth urls must come before site urls
urlpatterns = [
	path('admin/', include('project.admin.urls')),
	path('account/', include('account.urls')),
	path('data_selection/', include('data_selection.urls', namespace='data_selection')),
	path('', include('dataset.urls', namespace='dataset')),
	path('', include('api.urls')),
]
