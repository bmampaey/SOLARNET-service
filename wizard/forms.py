# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from wizard.models import UserDataSelection
from djorm_pgarray.fields import ArrayFormField

class Login(forms.Form):
	email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'my.email@address.com'}))

class DataSelectionCreateForm(forms.Form):
	user_data_selection_name = forms.CharField(help_text="The name for the selection", widget = forms.Select(choices=[]))
	dataset_name = forms.CharField(help_text="Name of the dataset for the selection", max_length=20, widget = forms.HiddenInput())
	query_string = forms.CharField(help_text="Query string for the data selection", max_length=2000, widget = forms.HiddenInput())
	all_selected = forms.BooleanField(help_text="Wheter all data was selected", required=False, widget = forms.HiddenInput())
	data_ids = ArrayFormField(help_text = "List of data ids to include or exclude (if all_selected is true)", required=False, widget = forms.MultipleHiddenInput())
	
	def __init__(self, user, *args, **kwargs):
		super(DataSelectionCreateForm, self).__init__(*args, **kwargs)
		self.fields['user_data_selection_name'].widget.choices = [(name, name) for name in UserDataSelection.objects.filter(user=user).values_list("name", flat=True)]