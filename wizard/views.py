import logging
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.core import urlresolvers

from wizard.forms import DatasetSearchForm
from dataset.models import Dataset

# Assert we only have get
@require_safe
def search_dataset(request):
	""" Generate the form to search dataset """
	
	#import pdb; pdb.set_trace()
	search_form = DatasetSearchForm(request.GET)
	if search_form.is_valid():
		selection_criteria = dict()
		if search_form.cleaned_data['telescope']:
			selection_criteria["telescope__in"]=search_form.cleaned_data['telescope']
		
		# Not necessary at the moment as we have only one dataset per instrument
		# if search_form.cleaned_data['instrument']:
		#	selection_criteria["instrument__in"]=search_form.cleaned_data['instrument']
		
		if search_form.cleaned_data['tags']:
			selection_criteria["tags__name__in"]=search_form.cleaned_data['tags']
		
		datasets = Dataset.objects.filter(**selection_criteria)
		headers = ["Data set", "Instrument", "Telescope", "Tags"]
		rows = list()
		for dataset in datasets:
			row = dict()
			try:
				row['href'] = urlresolvers.reverse('search_'+dataset.name)
				row['fields'] = [dataset.name, dataset.instrument, dataset.telescope, ", ".join(dataset.tags.names())]
				rows.append(row)
			except urlresolvers.NoReverseMatch, why:
				logging.error("No view found to search for dataset %s: %s", dataset.name, why)
		
		return render(request, 'wizard/search_dataset.html', {"search_form": search_form, "headers": headers, "rows": rows})
	
	else:
		return HttpResponseBadRequest(str(search_form.errors))

# Assert we only have get
@require_safe
def search_data(request, dataset_name):
	"""Call the appropriate view"""
	if dataset_name == "eit":
		return search_eit(request)
	elif dataset_name == "swap":
		return search_swap(request)
	else:
		return HttpResponseNotFound("Unknown dataset " + dataset_name)


# Assert we only have get
@require_safe
def download_data(request, dataset_name, data_id):
	"""Return the data"""
	return HttpResponseServerError("Not yet implemented")

from wizard.forms import EitSearchForm
import eit.models
# Assert we only have get
@require_safe
def search_eit(request):
	""" Generate the form to search the eit dataset """
	search_form = EitSearchForm(request.GET)
	if search_form.is_valid():
		selection_criteria = dict()
		
		if search_form.cleaned_data['start_date']:
			selection_criteria["date_obs__gte"]=search_form.cleaned_data['start_date']
		
		if search_form.cleaned_data['end_date']:
			selection_criteria["date_obs__lte"]=search_form.cleaned_data['end_date']
		
		if search_form.cleaned_data['wavelengths']:
			selection_criteria["wavelnth__in"]=search_form.cleaned_data['wavelengths']
		
		if search_form.cleaned_data['science_objectif']:
			selection_criteria["sci_obj__in"]=search_form.cleaned_data['science_objectif']
		
		data_selection = eit.models.MetaData.objects.filter(**selection_criteria).exclude(data_location__isnull=True)
		headers = ["Date Observation", "Wavelength", "Science Objectif", "Tags"]
		rows = list()
		for data in data_selection:
			row = dict()
			#row['href'] = urlresolvers.reverse('download', kwargs={'dataset': 'eit', 'id': data.id})
			row['href'] = data.data_location
			row['fields'] = [data.date_obs, data.wavelnth, data.sci_obj, ", ".join(data.tags.names())]
			rows.append(row)
		
		return render(request, 'wizard/search_dataset.html', {"search_form": search_form, "headers": headers, "rows": rows})
	
	else:
		return HttpResponseBadRequest(str(search_form.errors))

from wizard.forms import SwapSearchForm
import swap.models

# Assert we only have get
@require_safe
def search_swap(request):
	""" Generate the form to search dataset """


