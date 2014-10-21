from django.conf.urls import patterns, url, include

from dataset import views

urlpatterns = patterns('',
	url(r'^search_by_dataset_form$', views.search_by_dataset_form, name='search_by_dataset_form'),
	url(r'^search_by_dataset_results$', views.search_by_dataset_results, name='search_by_dataset_results'),
	url(r'^search_across_datasets_form$', views.search_across_datasets_form, name='search_across_datasets_form'),
	url(r'^search_across_datasets_results$', views.search_across_datasets_results, name='search_across_datasets_results'),
)
