# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms

from dataset.models import DataSet

INSTRUMENTS = DataSet.objects.order_by().values_list('instrument', flat = True).distinct()
TELESCOPES = DataSet.objects.order_by().values_list('telescope', flat = True).distinct()



class DataSetSearchForm(forms.Form):
	"""Form to search data sets"""
	instrument = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = INSTRUMENTS, choices=[(i, u'%s'%i) for i in INSTRUMENTS])
	telescope = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TELESCOPES, choices=[(t, u'%s'%t) for t in TELESCOPES])
#	tags = TaggableManager()

class TagSearchForm(forms.Form):
	"""Form to search data by tag"""
	pass
