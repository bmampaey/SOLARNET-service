import logging
from collections import OrderedDict

from django.views.generic import TemplateView, ListView, RedirectView
from django.core import urlresolvers
from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator
from common.django_paginator import EstimatedCountPaginator


# See links below for some explanations on class based views
# http://georgebrock.github.io/talks/intro-to-class-based-generic-views/
# https://blog.safaribooksonline.com/2013/10/28/class-based-views-in-django/
# https://github.com/django/django/blob/master/django/views/generic/list.py

class BaseSearchDataForm(TemplateView):
	search_form_class = None  #To be overriden in the derived class
	dataset_name = None # To be overriden in the derived class
	template_name = 'common/search_data_form.html'
	
	
	def get_context_data(self, **kwargs):
		context = super(BaseSearchDataForm, self).get_context_data(**kwargs)
		context['search_form'] = self.search_form_class(auto_id=self.dataset_name+'_%s')
		context['dataset_name'] = self.dataset_name
		return context


class BaseSearchDataResults(ListView):
	dataset_name = None # To be overriden in the derived class
	model = None # To be overriden in the derived class
	search_form_class = None # To be overriden in the derived class
	table_columns = OrderedDict([("date_obs", "Date Observation")]) # To be overriden in the derived class. Use an OrderedDict if you want the order of columns to be respected.
	paginate_by = 20
	paginate_orphans = 0
	context_object_name = 'data_list'
	paginator_class = Paginator # To be replaced by EstimatedCountPaginator
	ordering = 'date_obs'
	template_name = 'common/search_data_results.html'
	
	
	def get_queryset(self):
		# Get the cleaned data from the form
		cleaned_data = self.search_form_class.get_cleaned_data(self.request.GET)
		# What happens if an exception is raised
		
		# Make up the selection criteria from the cleaned data
		selection_criteria = self.search_form_class.get_selection_criteria(cleaned_data)
	
		# Return the the QuerySet for the meta-data
		# We exclude the ones where there is no data location associated (as it is not possible to download them)
		return self.model.objects.filter(**selection_criteria).exclude(data_location__isnull=True)
	
	def get_context_data(self, **kwargs):
		context = super(BaseSearchDataResults, self).get_context_data(**kwargs)
		context['dataset_name'] = self.dataset_name
		context['table_columns'] = self.table_columns
		
		# Set up the pages navigation by encoding the request data without the page number
		# The request data from a request is immutable, therefore we need to copy it
		query_dict = self.request.GET.copy()
		try:
			del query_dict[self.page_kwarg]
		except KeyError:
			pass
		context['query_string'] = query_dict.urlencode()
		context['page_kwarg'] = self.page_kwarg
		return context


class BaseDownloadData(RedirectView):
	data_location_model = None # To be overriden in the derived class
	permanent = True
	
	def get_redirect_url(self, data_id):
		data_location = get_object_or_404(self.data_location_model, meta_data_id=data_id)
		return data_location.url

