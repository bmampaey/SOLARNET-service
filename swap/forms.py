# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from django.contrib.contenttypes.models import ContentType

from common.forms import BaseForm
from swap.models import MetaData

class SearchForm(BaseForm):
	"""Form to search the dataset"""
	FIRST_DATE_OBS = MetaData.objects.order_by("date_obs").first().date_obs
	LAST_DATE_OBS = MetaData.objects.order_by("date_obs").last().date_obs
	start_date = forms.DateTimeField(required=False, initial = FIRST_DATE_OBS, widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	end_date = forms.DateTimeField(required=False, initial = LAST_DATE_OBS, widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	
	@classmethod
	def get_selection_criteria(cls, cleaned_data):
		"""Create and return a dictionary of selection criteria from the cleaned data"""
		selection_criteria = dict()
		
		if cleaned_data['start_date']:
			selection_criteria["date_obs__gte"] = cleaned_data['start_date']
		
		if cleaned_data['end_date']:
			selection_criteria["date_obs__lte"] = cleaned_data['end_date']
		
		return selection_criteria