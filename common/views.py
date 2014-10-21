import logging
from collections import OrderedDict

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView, RedirectView

from common.django_paginator import EstimatedCountPaginator






# Todo replace form by class based form and derive for each dataset (same for download)

class BaseSearchDataForm(TemplateView):
	template_name = 'common/search_data_form.html'
	form_class = None  #To be overriden in the derived class
	
	def get_context_data(self, **kwargs):
		import pdb; pdb.set_trace()
		context = super(BaseSearchDataForm, self).get_context_data(**kwargs)
		context['form'] = form_class()
		return context


class BaseSearchDataResults(ListView):
	model = None #To be overriden in the derived class
	paginate_by = 20
	paginate_orphans = 0
	context_object_name = 'data'
	paginator_class = Paginator # To be replaced by EstimatedCountPaginator
	ordering = 'date_obs'
	template_name = 'common/search_data_results.html'
	table_columns = OrderedDict([("date_obs", "Date Observation")])
	
	def get_queryset(self):
		# TODO https://github.com/django/django/blob/master/django/views/generic/list.py
		# http://georgebrock.github.io/talks/intro-to-class-based-generic-views/
		# https://blog.safaribooksonline.com/2013/10/28/class-based-views-in-django/
		pass
		
	def get_context_data(self, **kwargs):
		# TODO
		import pdb; pdb.set_trace()
		context = super(BaseSearchDataResults, self).get_context_data(**kwargs)
		
		# Get the cleaned data from the form
		try:
			cleaned_data = form_class.get_cleaned_data(request.GET)
		except Exception, why:
			return HttpResponseBadRequest(str(why))
		
		
		return context


class BaseDownloadData(RedirectView):
	data_location_model = None # To be overriden in the derived class
	permanent = True
	
	def get_redirect_url(data_id):
		data_location = get_object_or_404(data_location_model, id=data_id)
		return data_location.url

