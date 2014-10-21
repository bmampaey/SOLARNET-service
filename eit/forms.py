# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms

from common.forms import BaseForm
from eit.models import MetaData


class SearchData(BaseForm):
	"""Form to search the data"""
	FIRST_DATE_OBS = MetaData.objects.order_by("date_obs").first().date_obs
	LAST_DATE_OBS = MetaData.objects.order_by("date_obs").last().date_obs
	EIT_WAVELENGTHS = [171, 195, 284, 304]
	SCIENCE_OBJECTIVES = MetaData.objects.values_list('sci_obj', flat=True).distinct()
	start_date = forms.DateTimeField(required=False, initial = FIRST_DATE_OBS, widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	end_date = forms.DateTimeField(required=False, initial = LAST_DATE_OBS, widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	wavelengths = forms.TypedMultipleChoiceField(required=False, coerce=int, widget=forms.SelectMultiple(), initial = EIT_WAVELENGTHS, choices=[(w, u'%sÅ'%w) for w in EIT_WAVELENGTHS])
	science_objectif = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = SCIENCE_OBJECTIVES, choices=[(t, u'%s'%t) for t in SCIENCE_OBJECTIVES])
	
	@classmethod
	def get_selection_criteria(cls, cleaned_data):
		"""Create and return a dictionary of selection criteria from the cleaned data"""
		selection_criteria = dict()
		
		if cleaned_data['start_date']:
			selection_criteria["date_obs__gte"] = cleaned_data['start_date']
		
		if cleaned_data['end_date']:
			selection_criteria["date_obs__lte"] = cleaned_data['end_date']
		
		if cleaned_data['wavelengths']:
			selection_criteria["wavelnth__in"] = cleaned_data['wavelengths']
		
		if cleaned_data['science_objectif']:
			selection_criteria["sci_obj__in"] = cleaned_data['science_objectif']
		
		return selection_criteria
