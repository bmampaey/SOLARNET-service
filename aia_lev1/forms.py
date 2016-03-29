 # -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms

from common.forms import BaseForm,TagField
from aia_lev1.models import MetaData, Tag


class SearchData(BaseForm):
	"""Form to search the data"""
	FIRST_DATE_OBS = MetaData.objects.order_by('date_obs').values_list('date_obs', flat = True).first()
	LAST_DATE_OBS = MetaData.objects.order_by('date_obs').values_list('date_obs', flat = True).last()
	AIA_WAVELENGTHS = [94, 131, 171, 193, 211, 304, 335, 1600, 1700, 4500]
	TAGS = lambda: [(t, u'%s'%t) for t in Tag.objects.values_list("name", flat=True)]
	start_date = forms.DateTimeField(required=False, initial = FIRST_DATE_OBS, widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	end_date = forms.DateTimeField(required=False, initial = LAST_DATE_OBS, widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	wavelengths = forms.TypedMultipleChoiceField(required=False, coerce=int, widget=forms.SelectMultiple(), initial = AIA_WAVELENGTHS, choices=[(w, u'%sÅ'%w) for w in AIA_WAVELENGTHS])
	best_quality = forms.BooleanField(required=False, initial = False, help_text="Search results will only display data for which the quality keyword is 0")
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
		
		if cleaned_data['wavelengths']:
			selection_criteria["wavelnth__in"] = cleaned_data['wavelengths']
		
		if cleaned_data['best_quality']:
			selection_criteria['quality__exact'] = 0
		
		if cleaned_data['tags']:
			selection_criteria["tags__name__in"] = cleaned_data['tags']
		return selection_criteria
