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

