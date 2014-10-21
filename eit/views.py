import logging
from collections import OrderedDict
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django.core.urlresolvers as urlresolvers

from common.django_paginator import EstimatedCountPaginator
from eit.forms import SearchForm
from eit.models import MetaData, DataLocation

# Assert we only have get
@require_safe
def search_data_form(request):
	""" Generate the form to search data """
	
	return render(request, 'common/search_data_form.html', {"dataset_name": "eit", "search_form": SearchForm()})

# Assert we only have get
@require_safe
def search_data_results(request):
	""" Generate search data results table """
	#import pdb; pdb.set_trace()
	# Get the cleaned data from the form
	try:
		cleaned_data = SearchForm.get_cleaned_data(request.GET)
	except Exception, why:
		return HttpResponseBadRequest(str(why))
	
	# Make up the selection criteria from the cleaned data
	selection_criteria = SearchForm.get_selection_criteria(cleaned_data)
	
	# Get the QuerySet for the meta-data
	# We exclude the ones where there is no data location associated (as it is not possible to download them)
	data_selection = MetaData.objects.filter(**selection_criteria).exclude(data_location__isnull=True)
	
	
	paginator = Paginator(data_selection, request.GET.get("limit", 20), allow_empty_first_page = False) # TODO replace with EsimatedCountPaginator
	page_number = request.GET.get("page", 1)
	
	try:
		page = paginator.page(page_number)
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = None
		logging.debug("No result found for search criteria %s", selection_criteria)
	#import pdb; pdb.set_trace()
	fields = OrderedDict([("date_obs", "Date Observation"), ("wavelnth", "Wavelength"), ("sci_obj", "Science Objectif")])
	rows = list()
	if page is not None:
		for data in page.object_list:
			row = dict()
			row['data_id'] = data.id
			row['data_location'] = urlresolvers.reverse('eit:download_data', kwargs={'data_id': data.id})
			row['fields'] = [getattr(data, field_name) for field_name in fields.iterkeys()]
			row['tags'] = data.tags.names()
			rows.append(row)
	
	return render(request, 'common/search_data_results.html', {"dataset_name": "eit", "headers": fields.values(), "rows": rows})

# Assert we only have get
@require_safe
def download_data(request, data_id):
	""" Generate the form to search data """
	data_location = get_object_or_404(DataLocation, id=data_id)
	return redirect(data_location.url)

