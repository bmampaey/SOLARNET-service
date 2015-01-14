# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from wizard.models import UserDataSelection
from djorm_pgarray.fields import ArrayFormField

from wizard.models import DataSelection

class Login(forms.Form):
	email = forms.EmailField(required=True, max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'my.email@address.com'}))

class ArrayField(forms.Field):
	
	def __init__(self, *args, **kwargs):
		self.base_type = kwargs.pop('base_type')
		self.widget = forms.MultipleHiddenInput
		super(ArrayField, self).__init__(*args, **kwargs)

	def clean(self, value):
		for subvalue in value:
			self.base_type.validate(subvalue)
	
		return [self.base_type.clean(subvalue) for subvalue in value]

class DataSelectionCreateForm(forms.ModelForm):
	
	dataset_id = forms.CharField(help_text="Id of the dataset for the selection", max_length=20, widget = forms.HiddenInput())
	user_data_selection_name = forms.CharField(label="Create a new selection", initial = "new", max_length=80)
	selected_data_ids = ArrayField(help_text="Selected data ids to include into the selection", base_type=forms.IntegerField(), required=False)
	class Meta:
		model = DataSelection
		exclude = ('user_data_selection', 'dataset', 'data_ids')
		widgets = {
			'query_string' : forms.HiddenInput,
			'all_selected' : forms.HiddenInput,
		}

