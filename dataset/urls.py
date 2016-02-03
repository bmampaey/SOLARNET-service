from django.conf.urls import url

from dataset import views

urlpatterns = [
	url(r'^search_by_dataset_form$', views.SearchByDatasetForm.as_view(), name='search_by_dataset_form'),
	url(r'^search_by_dataset_results$', views.SearchByDatasetResults.as_view(), name='search_by_dataset_results'),
	url(r'^search_across_datasets_form$', views.SearchAcrossDatasetsForm.as_view(), name='search_across_datasets_form'),
	url(r'^search_across_datasets_results$', views.SearchAcrossDatasetsResults.as_view(), name='search_across_datasets_results'),
]
