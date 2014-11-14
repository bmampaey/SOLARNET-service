import logging
from collections import OrderedDict

from django.views.generic import TemplateView, ListView
from django.core import urlresolvers
from django.http import QueryDict

from dataset.forms import SearchByDataset, SearchAcrossDatasets
from dataset.models import Dataset




# See links below for some explanations on class based views
# http://georgebrock.github.io/talks/intro-to-class-based-generic-views/
# https://blog.safaribooksonline.com/2013/10/28/class-based-views-in-django/
# https://github.com/django/django/blob/master/django/views/generic/list.py

class SearchByDatasetForm(TemplateView):
	search_form_class = SearchByDataset
	template_name = 'dataset/search_by_dataset_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(SearchByDatasetForm, self).get_context_data(**kwargs)
		context['search_form'] = self.search_form_class()
		return context

class SearchAcrossDatasetsForm(TemplateView):
	search_form_class = SearchAcrossDatasets
	template_name = 'dataset/search_across_datasets_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(SearchAcrossDatasetsForm, self).get_context_data(**kwargs)
		context['search_form'] = self.search_form_class()
		return context

class SearchByDatasetResults(ListView):
	model = Dataset
	search_form_class = SearchByDataset
	table_columns = OrderedDict([('name', 'Dataset'), ('instrument', 'Instrument'), ('telescope', 'Telescope')])
	paginate_by = None # We do not paginate for datasets
	context_object_name = 'dataset_list'
	ordering = 'name'
	template_name = 'dataset/search_by_dataset_results.html'
	
	
	def get_queryset(self):
		# Get the cleaned data from the form
		cleaned_data = self.search_form_class.get_cleaned_data(self.request.GET)
		
		# Make up the selection criteria from the cleaned data
		selection_criteria = self.search_form_class.get_selection_criteria(cleaned_data)
	
		# Return the the QuerySet for the datasets
		return self.model.objects.filter(**selection_criteria).distinct()
	
	def get_context_data(self, **kwargs):
		context = super(SearchByDatasetResults, self).get_context_data(**kwargs)
		context['table_columns'] = self.table_columns
		return context

class SearchAcrossDatasetsResults(ListView):
	model = Dataset
	search_form_class = SearchAcrossDatasets
	table_columns = OrderedDict([('name', 'Dataset'), ('instrument', 'Instrument'), ('telescope', 'Telescope')])
	paginate_by = None # We do not paginate for datasets
	context_object_name = 'dataset_list'
	ordering = 'name'
	template_name = 'dataset/search_across_datasets_results.html'
	
	
	def get_queryset(self):
		import pdb; pdb.set_trace()
		
		# Get the cleaned data from the form
		cleaned_data = self.search_form_class.get_cleaned_data(self.request.GET)
		
		# Make up the selection criteria from the cleaned data
		selection_criteria = self.search_form_class.get_selection_criteria(cleaned_data)
		
		# Return the the QuerySet for the datasets
		datasets = list()
		for dataset in self.model.objects.filter(**selection_criteria).distinct():
			query = QueryDict("",mutable=True)
			if(cleaned_data['tags']):
				# TODO make sure that the records with more than 1 tags are not duplicated and make sure that a data location exists
				item_count = dataset.tag_model.objects.filter(name__in=cleaned_data['tags']).count()
				query['tags'] = cleaned_data['tags']
			else:
				item_count = dataset.data_location_model.objects.count()
			
			if item_count > 0:
				dataset.item_count = item_count
				dataset.query_string = query.urlencode()
				datasets.append(dataset)
		
		return datasets
	
	def get_context_data(self, **kwargs):
		context = super(SearchAcrossDatasetsResults, self).get_context_data(**kwargs)
		context['table_columns'] = self.table_columns
		return context



