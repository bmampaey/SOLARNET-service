from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from tastypie.validation import FormValidation
from django.forms import ModelForm

from SDA.resources import ResourceMeta
from dataset.models import Dataset, Characteristic, Instrument, Telescope, Keyword

class TelescopeResource(ModelResource):
	'''RESTful resource for model Telescope'''
	instruments = fields.ToManyField('dataset.resources.InstrumentResource', 'instruments', related_name='name', full = True)
	
	class Meta(ResourceMeta):
		queryset = Telescope.objects.all()
		resource_name = 'telescope'
		allowed_methods = ['get']
		max_limit = None
		limit = None
		filtering = {
			"name": ALL,
			"description": ALL,
		}



class InstrumentResource(ModelResource):
	'''RESTful resource for model Instrument'''
	telescope = fields.ForeignKey(TelescopeResource, 'telescope', full = False)
	
	class Meta(ResourceMeta):
		queryset = Instrument.objects.all()
		resource_name = 'instrument'
		allowed_methods = ['get']
		max_limit = None
		limit = None
		filtering = {
			"name": ALL,
			"description": ALL,
		}



class CharacteristicResource(ModelResource):
	'''RESTful resource for model Characteristic'''
	
	class Meta(ResourceMeta):
		queryset = Characteristic.objects.all()
		resource_name = 'characteristic'
		allowed_methods = ['get']
		max_limit = None
		limit = None


class KeywordValidationForm(ModelForm):
	'''RESTful resource for model Keyword'''
	
	class Meta(ResourceMeta):
		model = Keyword
		fields = '__all__'

class KeywordResource(ModelResource):
	'''RESTful resource for model Keyword'''
	
	class Meta(ResourceMeta):
		queryset = Keyword.objects.all()
		resource_name = 'keyword'
		allowed_methods = ['get']
		# TODO test validation
		#validation = FormValidation(KeywordValidationForm())



class DatasetResource(ModelResource):
	'''RESTful resource for model Dataset'''
	characteristics = fields.ToManyField(CharacteristicResource, 'characteristics', full = False)
	#TODO check here
#	characteristics = fields.ListField()
	instrument = fields.CharField('instrument')
	telescope = fields.CharField('telescope')
	
	class Meta(ResourceMeta):
		queryset = Dataset.objects.all()
		resource_name = 'dataset'
		allowed_methods = ['get']
		max_limit = None
		limit = None
		filtering = {
			"name": ALL,
			"description": ALL,
			"contact": ALL,
			"instrument": ALL,
			"telescope": ALL,
			"characteristics": ALL_WITH_RELATIONS
		}
		
	def dehydrate(self, bundle):
		#TODO check here
		# bundle.data['characteristics'] = [str(name) for name in bundle.obj.characteristics.values_list('name', flat = True)]
		return bundle

