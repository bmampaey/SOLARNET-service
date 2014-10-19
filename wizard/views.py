import logging
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.core import urlresolvers


# Assert we only have get
@require_safe
def index(request):
	"""TODO"""
	return render(request, 'wizard/index.html', {})


# Assert we only have get
@require_safe
def search_data(request, dataset_name):
	"""Call the appropriate view"""
	if dataset_name == "eit":
		import eit.views
		return eit.views.search_data(request)
	elif dataset_name == "swap":
		import swap.views
		return swap.views.search_data(request)
	else:
		return HttpResponseNotFound("Unknown dataset " + dataset_name)

# Assert we only have get
@require_safe
def download_data(request, dataset_name, data_id):
	if dataset_name == "eit":
		import eit.models
		data_location = get_object_or_404(eit.models.DataLocation.get, id=data_id)
	elif dataset_name == "swap":
		import swap.models
		data_location = get_object_or_404(swap.models.DataLocation.get, id=data_id)
	else:
		return HttpResponseNotFound("Unknown dataset " + dataset_name)
	
	redirect(data_location.url)
