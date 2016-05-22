from django.contrib.admin.helpers import ActionForm
from django import forms
from metadata.models import Tag

class AddTagForm(ActionForm):
	'''Form for the add tag action of the  admin class for the Metadta models'''
	tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required = False)