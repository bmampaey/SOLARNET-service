# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from django.contrib.contenttypes.models import ContentType

from common.forms import BaseForm
from taggit.models import TaggedItem
from dataset.models import Dataset


class DatasetSearchForm(BaseForm):
	"""Form to search data sets"""
	TELESCOPES = Dataset.objects.order_by().values_list('telescope', flat = True).distinct()
	INSTRUMENTS = Dataset.objects.order_by().values_list('instrument', flat = True).distinct()
	INSTRUMENTS_BY_TELESCOPE = [(t, [(i, u'%s'%i) for i in Dataset.objects.order_by().filter(telescope = t).values_list('instrument', flat = True).distinct()]) for t in TELESCOPES]
	TAGS = TaggedItem.objects.filter(content_type_id = ContentType.objects.get_for_model(Dataset).id).values_list('tag__name', flat=True).distinct()
	instrument = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = INSTRUMENTS, choices=INSTRUMENTS_BY_TELESCOPE)
	#telescope = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TELESCOPES, choices=[(t, u'%s'%t) for t in TELESCOPES])
	tags = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TAGS, choices=[(t, u'%s'%t) for t in TAGS])


class TagSearchForm(BaseForm):
	"""Form to search data by tag"""
	pass
