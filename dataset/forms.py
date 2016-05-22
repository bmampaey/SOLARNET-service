from django import forms
from django.contrib.contenttypes.models import ContentType
from dataset.models import Dataset

class DatasetAdminForm(forms.ModelForm):
	'''Form for the admin class for the Dataset model'''
	# Display app label via the ContentTypeChoiceField, and limit to model Metadata (must be in lowcase as it is saved in lowcase)
	_metadata_model = forms.ModelChoiceField(queryset=ContentType.objects.filter(app_label='metadata').exclude(model='tag')) 
	class Meta:
		model = Dataset
		fields = '__all__'