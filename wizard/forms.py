# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from django.contrib.contenttypes.models import ContentType

from taggit.models import TaggedItem

from dataset.models import DataSet
from taggit.models import Tag

INSTRUMENTS = DataSet.objects.order_by().values_list('instrument', flat = True).distinct()
TELESCOPES = DataSet.objects.order_by().values_list('telescope', flat = True).distinct()
TAGS = TaggedItem.objects.filter(content_type_id = ContentType.objects.get_for_model(DataSet).id).values_list('tag__name', flat=True).distinct()



class DataSetSearchForm(forms.Form):
	"""Form to search data sets"""
	instrument = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = INSTRUMENTS, choices=[(i, u'%s'%i) for i in INSTRUMENTS])
	telescope = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TELESCOPES, choices=[(t, u'%s'%t) for t in TELESCOPES])
	tags = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TAGS, choices=[(t, u'%s'%t) for t in TAGS])
	
	@classmethod
	def initials(cls):
		data = dict()
		for name, field in cls.base_fields.iteritems():
			data[name] = field.initial
		return data

class TagSearchForm(forms.Form):
	"""Form to search data by tag"""
	pass
