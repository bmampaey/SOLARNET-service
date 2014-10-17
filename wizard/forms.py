# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from django.contrib.contenttypes.models import ContentType

from taggit.models import TaggedItem

from dataset.models import Dataset
from taggit.models import Tag



class BaseForm(forms.Form):
	"""Base form to set common methods and parameters to all forms"""
	
	@classmethod
	def initials(cls):
		data = dict()
		for name, field in cls.base_fields.iteritems():
			data[name] = field.initial
		return data


class DatasetSearchForm(BaseForm):
	"""Form to search data sets"""
	INSTRUMENTS = Dataset.objects.order_by().values_list('instrument', flat = True).distinct()
	TELESCOPES = Dataset.objects.order_by().values_list('telescope', flat = True).distinct()
	TAGS = TaggedItem.objects.filter(content_type_id = ContentType.objects.get_for_model(Dataset).id).values_list('tag__name', flat=True).distinct()
	#instrument = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = INSTRUMENTS, choices=[(i, u'%s'%i) for i in INSTRUMENTS])
	telescope = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TELESCOPES, choices=[(t, u'%s'%t) for t in TELESCOPES])
	tags = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TAGS, choices=[(t, u'%s'%t) for t in TAGS])


class TagSearchForm(BaseForm):
	"""Form to search data by tag"""
	pass


import eit.models
class EitSearchForm(BaseForm):
	"""Form to search eit dataset"""
	EIT_WAVELENGTHS = [171, 195, 284, 304]
	SCIENCE_OBJECTIVES = eit.models.MetaData.objects.values_list('sci_obj', flat=True).distinct()
	start_date = forms.DateTimeField(required=False, initial = datetime(1996, 01, 01), widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	end_date = forms.DateTimeField(required=False, initial = datetime(1996, 01, 02), widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	wavelengths = forms.TypedMultipleChoiceField(required=False, coerce=int, widget=forms.SelectMultiple(), initial = EIT_WAVELENGTHS, choices=[(w, u'%sÅ'%w) for w in EIT_WAVELENGTHS])
	science_objectif = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = SCIENCE_OBJECTIVES, choices=[(t, u'%s'%t) for t in SCIENCE_OBJECTIVES])

import swap.models
class SwapSearchForm(BaseForm):
	"""Form to search swap dataset"""
	start_date = forms.DateTimeField(required=False, initial = datetime(1996, 01, 01), widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))
	end_date = forms.DateTimeField(required=False, initial = datetime.utcnow(), widget=forms.DateTimeInput(format = "%Y-%m-%d %H:%M:%S", attrs={'class': 'date_time_input'}))

