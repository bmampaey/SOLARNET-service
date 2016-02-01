import floppyforms.__future__ as forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form, AuthenticationForm):
	username = forms.CharField(max_length=254)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
