# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from django.contrib.contenttypes.models import ContentType
from taggit.models import TaggedItem

from common.forms import BaseForm
from dataset.models import Dataset, DatasetCharacteristic


class SearchByDataset(BaseForm):
	"""Form to search by dataset"""
	TELESCOPES = Dataset.objects.order_by().values_list('telescope', flat = True).distinct()
	INSTRUMENTS = Dataset.objects.order_by().values_list('instrument', flat = True).distinct()
	INSTRUMENTS_BY_TELESCOPE = [(t, [(i, u'%s'%i) for i in Dataset.objects.order_by().filter(telescope = t).values_list('instrument', flat = True).distinct()]) for t in TELESCOPES]
	CHARACTERISTICS = DatasetCharacteristic.objects.values_list('tag__name', flat=True).distinct()
	instrument = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = INSTRUMENTS, choices=INSTRUMENTS_BY_TELESCOPE)
	characteristics = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = CHARACTERISTICS, choices=[(t, u'%s'%t) for t in CHARACTERISTICS])
	
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
	CHARACTERISTICS = DatasetCharacteristic.objects.values_list('tag__name', flat=True).distinct()
	# Absolutely all tags from all datasets
	TAGS = set([tag for tags in [ TaggedItem.objects.filter(content_type_id = ContentType.objects.get(model = 'metadata', app_label=dataset.name).id).values_list('tag__name', flat=True).distinct() for dataset in  Dataset.objects.all()] for tag in tags])
	characteristics = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = CHARACTERISTICS, choices=[(t, u'%s'%t) for t in CHARACTERISTICS])
	tags = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TAGS, choices=[(t, u'%s'%t) for t in TAGS])
	
	@classmethod
	def get_selection_criteria(cls, cleaned_data):
		"""Create and return a dictionary of selection criteria from the cleaned data"""
		selection_criteria = dict()
		
		if cleaned_data['characteristics']:
			selection_criteria["characteristics__name__in"]=cleaned_data['characteristics']
		
		if cleaned_data['tags']:
			dataset_ids = 
			selection_criteria["tags__name__in"]=cleaned_data['tags']
		
		return selection_criteria
