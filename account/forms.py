import floppyforms.__future__ as forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
	email = forms.EmailField(required=True, max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'my.email@address.com'}))
