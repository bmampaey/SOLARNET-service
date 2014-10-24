# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms

class Login(forms.Form):
	email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'my.email@address.com'}))

