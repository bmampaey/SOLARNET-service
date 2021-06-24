from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.utils.functional import cached_property

__all__ = ['Dataset']

class DatasetManager(models.Manager):
	'''Manager that optimize the queries by selecting the foreign objects'''
	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.select_related('telescope', 'instrument', 'user_group').prefetch_related('characteristics')
		return queryset
		
	def get_by_natural_key(self, name):
		return self.get(name=name)

class Dataset(models.Model):
	'''Model for the description of a dataset'''
	name = models.CharField(max_length = 200, unique = True, help_text = 'Can contain any unicode character')
	description = models.TextField(blank = True, null = True, help_text = 'Can contain html with links, emphasis, etc.')
	contact_email = models.EmailField(help_text = 'Email of the dataset archive contact person', blank = True, null = True)
	archive_url = models.URLField(help_text = 'Official URL of the dataset archive', max_length = 2000, blank = True, null = True)
	telescope = models.ForeignKey('Telescope', on_delete = models.PROTECT, related_name = 'datasets')
	instrument = models.ForeignKey('Instrument', on_delete = models.PROTECT, related_name = 'datasets')
	characteristics = models.ManyToManyField('Characteristic', related_name = 'datasets', blank = True)
	user_group = models.ForeignKey('auth.Group', on_delete = models.SET_NULL, related_name = 'user_groups', help_text = 'User of this group can modify the dataset', blank = True, null = True)
	metadata_content_type = models.OneToOneField(ContentType, on_delete = models.SET_NULL, limit_choices_to = models.Q(app_label = 'metadata') & ~models.Q(model = 'tag'), help_text = 'The model for this dataset metadata', blank = True, null = True, unique=True)
	
	objects = DatasetManager()
	
	class Meta:
		ordering = ['name']
		verbose_name = 'Dataset'
	
	def __str__(self):
		return self.name
	
	def natural_key(self):
		return self.name
	
	@cached_property
	def metadata_model(self):
		if self.metadata_content_type is None:
			raise ValueError('metadata_content_type has not been set for this dataset')
		else:
			return self.metadata_content_type.model_class()
