import logging
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.core import urlresolvers

from dataset.forms import DatasetSearchForm
from dataset.models import Dataset

# Assert we only have get
@require_safe
def search_dataset(request):
	""" Generate the form to search dataset """
	
	#import pdb; pdb.set_trace()
	search_form = DatasetSearchForm(request.GET)
	if search_form.is_valid():
		selection_criteria = dict()
		
		# Not necessary at the moment as we have only one dataset per instrument
		# if search_form.cleaned_data['telescope']:
		#	selection_criteria["telescope__in"]=search_form.cleaned_data['telescope']
		
		if search_form.cleaned_data['instrument']:
			selection_criteria["instrument__in"]=search_form.cleaned_data['instrument']
		
		if search_form.cleaned_data['tags']:
			selection_criteria["tags__name__in"]=search_form.cleaned_data['tags']
		
		datasets = Dataset.objects.filter(**selection_criteria)
		headers = ["Data set", "Instrument", "Telescope", "Tags"]
		rows = list()
		for dataset in datasets:
			row = dict()
			try:
				row['href'] = urlresolvers.reverse('search_data', kwargs = {'dataset_name': dataset.name})
				row['fields'] = [dataset.name, dataset.instrument, dataset.telescope, ", ".join(dataset.tags.names())]
				rows.append(row)
			except urlresolvers.NoReverseMatch, why:
				logging.error("No view found to search for dataset %s: %s", dataset.name, why)
		
		return render(request, 'wizard/search_dataset.html', {"search_form": search_form, "headers": headers, "rows": rows})
	
	else:
		return HttpResponseBadRequest(str(search_form.errors))

