# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from django.contrib.contenttypes.models import ContentType

from common.forms import BaseForm
from common.models import Tag
from dataset.models import Dataset, Characteristic


class SearchByDataset(BaseForm):
	"""Form to search by dataset"""
#	TELESCOPES = Dataset.objects.order_by().values_list('telescope', flat = True).distinct()
#	INSTRUMENTS = Dataset.objects.order_by().values_list('instrument', flat = True).distinct()
#	INSTRUMENTS_BY_TELESCOPE = [(t, [(i, u'%s'%i) for i in Dataset.objects.order_by().filter(telescope = t).values_list('instrument', flat = True).distinct()]) for t in TELESCOPES]
#	CHARACTERISTICS = Characteristic.objects.values_list('name', flat=True)
#	instrument = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), choices=INSTRUMENTS_BY_TELESCOPE)
#	characteristics = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), choices=[(t, u'%s'%t) for t in CHARACTERISTICS])
	
	@classmethod
	def get_selection_criteria(cls, cleaned_data):
		"""Create and return a dictionary of selection criteria from the cleaned data"""
		selection_criteria = dict()
		
		if cleaned_data['instrument']:
			selection_criteria["instrument__in"]=cleaned_data['instrument']
		
		if cleaned_data['characteristics']:
			selection_criteria["characteristics__name__in"]=cleaned_data['characteristics']
		
		return selection_criteria


class SearchAcrossDatasets(BaseForm):
	"""Form to search across datasets"""
	characteristics = forms.ModelMultipleChoiceField(queryset = Characteristic.objects.all(), required=False, widget=forms.SelectMultiple())
	start_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	end_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	tags = forms.ModelMultipleChoiceField(queryset = Tag.objects.all(), required=False)
	
#	# Overiding init to load choices dynamically
#	# When django 1.8 is out, you can use the callable directly for the choices
#	def __init__(self, *args, **kwargs):
#		super(SearchAcrossDatasets, self).__init__(*args, **kwargs)
#		self.fields['characteristics'].choices = [(t, u'%s'%t) for t in Characteristic.objects.values_list('name', flat=True)]
#		self.fields['tags'].choices = [(t, u'%s'%t) for t in BaseTag.all_tags()]
	
	@classmethod
	def get_selection_criteria(cls, cleaned_data):
		"""Create and return a dictionary of selection criteria from the cleaned data"""
		selection_criteria = dict()
		
		if cleaned_data['characteristics']:
			selection_criteria["characteristics__name__in"]=cleaned_data['characteristics']
		
		return selection_criteria
