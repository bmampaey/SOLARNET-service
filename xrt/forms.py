# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms

from common.forms import BaseForm, TagField
from xrt.models import MetaData, Tag


class SearchData(BaseForm):
	"""Form to search the data"""
	FIRST_DATE_OBS = MetaData.objects.order_by('date_obs').values_list('date_obs', flat = True).first()
	LAST_DATE_OBS = MetaData.objects.order_by('date_obs').values_list('date_obs', flat = True).last()
	TAGS = lambda: [(t, u'%s'%t) for t in Tag.objects.values_list("name", flat=True)]
	NOAA_NUM = MetaData.objects.filter(noaa_num__gt=0).values_list('noaa_num', flat = True).distinct()
	TARGET = MetaData.objects.exclude(target='').values_list('target', flat = True).distinct()
	start_date = forms.DateTimeField(required=False, initial = FIRST_DATE_OBS, widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	end_date = forms.DateTimeField(required=False, initial = LAST_DATE_OBS, widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	noaa_num = forms.TypedMultipleChoiceField(required=False, coerce=int, widget=forms.SelectMultiple(), initial = NOAA_NUM, choices=[(w, u'%s'%w) for w in NOAA_NUM])
	target = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TARGET, choices=[(w, w) for w in TARGET])
	tags = TagField(required=False, choices=TAGS())
	
	
	# Overiding init to load choices dynamically
	# When django 1.8 is out, you can use the callable directly for the choices
	def __init__(self, *args, **kwargs):
		super(SearchData, self).__init__(*args, **kwargs)
		self.fields['tags'].choices = [(t, u'%s'%t) for t in Tag.objects.values_list("name", flat=True)]
	
	@classmethod
	def get_selection_criteria(cls, cleaned_data):
		"""Create and return a dictionary of selection criteria from the cleaned data"""
		selection_criteria = dict()
		
		if cleaned_data['start_date']:
			selection_criteria["date_obs__gte"] = cleaned_data['start_date']
		
		if cleaned_data['end_date']:
			selection_criteria["date_obs__lte"] = cleaned_data['end_date']
		
		if cleaned_data['noaa_num']:
			selection_criteria["noaa_num__in"] = cleaned_data['noaa_num']
		
		if cleaned_data['target']:
			selection_criteria["target__in"] = cleaned_data['target']
		
		if cleaned_data['tags']:
			selection_criteria["tags__name__in"] = cleaned_data['tags']
		
		return selection_criteria
