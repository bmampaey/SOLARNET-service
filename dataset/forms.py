# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from django.contrib.contenttypes.models import ContentType

from common.forms import BaseForm
from taggit.models import TaggedItem
from dataset.models import Dataset


class SearchByDatasetForm(BaseForm):
	"""Form to search by dataset"""
	TELESCOPES = Dataset.objects.order_by().values_list('telescope', flat = True).distinct()
	INSTRUMENTS = Dataset.objects.order_by().values_list('instrument', flat = True).distinct()
	INSTRUMENTS_BY_TELESCOPE = [(t, [(i, u'%s'%i) for i in Dataset.objects.order_by().filter(telescope = t).values_list('instrument', flat = True).distinct()]) for t in TELESCOPES]
	CHARACTERISTICS = TaggedItem.objects.filter(content_type_id = ContentType.objects.get_for_model(Dataset).id).values_list('tag__name', flat=True).distinct()
	instrument = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = INSTRUMENTS, choices=INSTRUMENTS_BY_TELESCOPE)
	characteristics = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = CHARACTERISTICS, choices=[(t, u'%s'%t) for t in CHARACTERISTICS])


class SearchAcrossDatasetsForm(BaseForm):
	"""Form to search across datasets"""
	CHARACTERISTICS = TaggedItem.objects.filter(content_type_id = ContentType.objects.get_for_model(Dataset).id).values_list('tag__name', flat=True).distinct()
	# Absolutely all tags from all datasets
	TAGS = set([tag for tags in [ TaggedItem.objects.filter(content_type_id = ContentType.objects.get(model = 'metadata', app_label=dataset.name).id).values_list('tag__name', flat=True).distinct() for dataset in  Dataset.objects.all()] for tag in tags])
	characteristics = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TAGS, choices=[(t, u'%s'%t) for t in TAGS])
	tags = forms.TypedMultipleChoiceField(required=False, widget=forms.SelectMultiple(), initial = TAGS, choices=[(t, u'%s'%t) for t in TAGS])
