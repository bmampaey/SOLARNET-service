from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_safe, require_POST, require_http_methods

from wizard.forms import DataSetSearchForm
from dataset.models import DataSet

# Assert we only have get
@require_safe
def search_data_set(request):
	""" Generate the form to search dataset """
	
	data_sets = get_list_or_404(DataSet)
	#import pdb; pdb.set_trace()
	search_form = DataSetSearchForm(request.GET)
	
	selection_criteria = dict()
	if search_form.is_valid():
		if search_form.cleaned_data['telescope']:
			selection_criteria["telescope__in"]=search_form.cleaned_data['telescope']
		
		if search_form.cleaned_data['instrument']:
			selection_criteria["instrument__in"]=search_form.cleaned_data['instrument']
		
		if search_form.cleaned_data['tags']:
			selection_criteria["tags__name__in"]=search_form.cleaned_data['tags']
		
		data_sets = DataSet.objects.filter(**selection_criteria)
		headers = ["Data set", "Instrument", "Telescope", "Tags"]
		rows = [(data_set.name, data_set.instrument, data_set.telescope, ", ".join(data_set.tags.names())) for data_set in data_sets]
		
		return render(request, 'wizard/search_data_set.html', {"search_form": search_form, "headers": headers, "rows": rows})
	
	else:
		return HttpResponseBadRequest(str(search_form.errors))

# Assert we only have get
@require_safe
def search_data_set_form(request):
	""" Generate the form to search dataset """
	
	data_sets = get_list_or_404(DataSet)
	
	search_form = DataSetSearchForm()
	
	return render(request, 'wizard/search_data_set_form.html', {"search_form": search_form})

# Assert we only have get
@require_safe
def search_data_set_results(request):
	""" Generate the result of a data set search"""
	
	search_form = DataSetSearchForm(request.GET)
	if search_form.is_valid():
		selection_criteria = dict()
		if search_form.cleaned_data['telescope']:
			selection_criteria["telescope__in"]=search_form.cleaned_data['telescope']
		
		if search_form.cleaned_data['instrument']:
			selection_criteria["instrument__in"]=search_form.cleaned_data['instrument']
		
		if search_form.cleaned_data['tags']:
			selection_criteria["tags__name__in"]=search_form.cleaned_data['tags']
		
		data_sets = get_list_or_404(DataSet, **selection_criteria)
		headers = ["Data set", "Instrument", "Telescope", "Tags"]
		rows = [(data_set.name, data_set.instrument, data_set.telescope, ", ".join(data_set.tags.names())) for data_set in data_sets]
		return render(request, 'wizard/search_data_set_results.html', {"headers": headers, "rows": rows})
	
	else:
		return HttpResponseBadRequest(str(search_form.errors))
	


