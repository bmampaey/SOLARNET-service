import logging
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.core import urlresolvers

from dataset.forms import SearchByDatasetForm, SearchAcrossDatasetsForm
from dataset.models import Dataset

# Assert we only have get
@require_safe
def search_by_dataset_form(request):
	""" Generate the form to search dataset """
	
	return render(request, 'dataset/search_by_dataset_form.html', {"search_form": SearchByDatasetForm()})


# Assert we only have get
@require_safe
def search_by_dataset_results(request):
	#import pdb; pdb.set_trace()
	search_form = SearchByDatasetForm(request.GET)
	if search_form.is_valid():
		selection_criteria = dict()
		
		if search_form.cleaned_data['instrument']:
			selection_criteria["instrument__in"]=search_form.cleaned_data['instrument']
		
		if search_form.cleaned_data['characteristics']:
			selection_criteria["characteristics__name__in"]=search_form.cleaned_data['characteristics']
		
		datasets = Dataset.objects.filter(**selection_criteria)
		headers = ["Data set", "Instrument", "Telescope", "Characteristics"]
		rows = list()
		for dataset in datasets:
			row = dict()
			try:
				row['href'] = urlresolvers.reverse('search_data_form', current_app = dataset.name)
				row['fields'] = [dataset.name, dataset.instrument, dataset.telescope, ", ".join(dataset.characteristics.names())]
				rows.append(row)
			except urlresolvers.NoReverseMatch, why:
				logging.error("No view found to search data for %s: %s", dataset.name, why)
		
		return render(request, 'dataset/search_by_dataset_results.html', {"headers": headers, "rows": rows})
	
	else:
		return HttpResponseBadRequest(str(search_form.errors))


# Assert we only have get
@require_safe
def search_across_datasets_form(request):
	""" Generate the form to search dataset """
	
	return render(request, 'dataset/search_across_datasets_form.html', {"search_form": SearchByDatasetForm()})


# Assert we only have get
@require_safe
def search_across_datasets_results(request):
	#import pdb; pdb.set_trace()
	search_form = SearchByDatasetForm(request.GET)
	if search_form.is_valid():
		selection_criteria = dict()
		
		if search_form.cleaned_data['characteristics']:
			selection_criteria["characteristics__name__in"]=search_form.cleaned_data['characteristics']
		
		if search_form.cleaned_data['tags']:
			#tag for tags in TaggedItem.objects.filter(content_type_id = ContentType.objects.get(model = 'metadata', app_label=dataset.name).id).values_list('tag__name', flat=True).distinct() for dataset in Dataset.objects.all()
			selection_criteria["tags__name__in"]=search_form.cleaned_data['tags']
		
		datasets = Dataset.objects.filter(**selection_criteria)
		headers = ["Count", "Data set", "Instrument", "Telescope", "Characteristics"]
		rows = list()
		for dataset in datasets:
			row = dict()
			try:
				row['href'] = urlresolvers.reverse('search_data_form', current_app = dataset.name)
				row['fields'] = [dataset.name, dataset.instrument, dataset.telescope, ", ".join(dataset.tags.names())]
				rows.append(row)
			except urlresolvers.NoReverseMatch, why:
				logging.error("No view found to search data for %s: %s", dataset.name, why)
		
		return render(request, 'dataset/search_across_datasets_results.html', {"headers": headers, "rows": rows})
	
	else:
		return HttpResponseBadRequest(str(search_form.errors))


