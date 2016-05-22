from django.contrib.admin.helpers import ActionForm
from django import forms
from metadata.models import Tag

class MultipleChoiceFieldNoValidation(forms.MultipleChoiceField):
	'''Choice field that does not do choice validation, with hidden inpu'''
	widget = forms.MultipleHiddenInput
	def validate(self, value):
		pass

class AddTagForm(ActionForm):
	'''Form for the add tag action of the  admin class for the Metadta models'''
	# Make the action hidden
	action = forms.CharField(widget=forms.HiddenInput())
	# Field that holds the selection
	# No need to validate as it is done by the admin framework
	_selected_action = MultipleChoiceFieldNoValidation()
	tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required = False, help_text="Select tags to add")