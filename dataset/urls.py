from django.conf.urls import patterns, url, include

from dataset import views

urlpatterns = patterns('',
	url(r'^search_dataset$', views.search_dataset, name='search_dataset'),
)
