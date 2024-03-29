import re
import sys
from django.core.management.base import BaseCommand, CommandError
from django.template import Template, Context
from django.conf import settings

from dataset.models import Dataset, KeywordType
from project.utils import Logger

# If you edit this file, increase the version
VERSION = '1'

# Mapping of the keyword type to the model field
MODEL_FIELD_MAP = {
	KeywordType.TEXT: 'models.TextField',
	KeywordType.TIME_ISO_8601: 'models.DateTimeField',
	KeywordType.INTEGER: 'models.BigIntegerField',
	KeywordType.REAL: 'models.FloatField',
	KeywordType.BOOLEAN: 'models.BooleanField',
}

# Template for the model file
MODEL_FILE_TEMPLATE = '''{% autoescape off %}# Generated by command {{ command }}
from django.db import models

from .base_metadata import BaseMetadata

__all__ = ['{{ model_name }}']

class {{ model_name }}(BaseMetadata):
	\'\'\'Model for the metadata of dataset {{ dataset.name }}\'\'\'
	
	class Meta(BaseMetadata.Meta):
		verbose_name = '{{ dataset.name|addslashes }} metadata'
		verbose_name_plural = '{{ dataset.name|addslashes }} metadata'
	{% for keyword in keywords %}
	{{ keyword.name }} = {{ keyword.model_field }}(verbose_name = '{{ keyword.verbose_name|addslashes }}', help_text='{{ keyword.description|default_if_none:""|addslashes }}', blank=True, null=True){% endfor %}
{% endautoescape %}'''

# Template for the resource file
RESOURCE_FILE_TEMPLATE = '''{% autoescape off %}# Generated by command {{ command }}
from metadata.models import {{ model_name }}
from .base_metadata import BaseMetadataResource

__all__ = ['{{ model_name }}Resource']


class {{ model_name }}Resource(BaseMetadataResource):
	\'\'\'RESTful resource for model {{ model_name }}\'\'\'
	
	class Meta(BaseMetadataResource.Meta):
		abstract = False
		queryset = {{ model_name }}.objects.all()
		resource_name = '{{ resource_name }}'
{% endautoescape %}'''

# Template for the admin file
ADMIN_FILE_TEMPLATE = '''{% autoescape off %}# Generated by command {{ command }}
from project import admin
from metadata.models import {{ model_name }}
from .base_metadata import BaseMetadataAdmin

__all__ = ['{{ model_name }}Admin']

@admin.register({{ model_name }})
class {{ model_name }}Admin(BaseMetadataAdmin):
	pass
{% endautoescape %}'''

# A little reminder to the admin ;)
EPILOGUE = '''DO NOT FORGET:
	1. Import the model in the models/__init__.py file, the resource in the resources/__init__.py and the admin in the admin/__init__.py file
	2. Create the metadata DB tables: ./manage.py makemigrations metadata && ./manage.py migrate metadata
	3. Set the dataset metadata_content_type to the metadata model via the admin interface
	4. Register the resource with the svo_api in metadata/urls.py
'''

class Command(BaseCommand):
	help = 'Generate the model, admin and resource files for the metadata corresponding to a dataset'
	
	def add_arguments(self, parser):
		parser.add_argument('dataset', help='The name of the dataset')
		parser.add_argument('--model_name', '-m', metavar='NAME', help='The name of the class for the metadata model')
		parser.add_argument('--resource_name', '-r', metavar='NAME', help='The name of the resource for the metadata resource')
		parser.add_argument('--file_name', '-f', metavar='FILENAME', help='The name of the model, resource and admin files')
		parser.add_argument('--overwrite', action = 'store_true', help='Overwrite the files')
	
	def handle(self, **options):
		# Create a logger
		self.log = Logger(self, options.get('verbosity', 2))
		
		# Set the command name and version
		self.command_name = '%s version %s' % (sys.argv[1], VERSION)
		
		# Get the dataset
		try:
			dataset = Dataset.objects.get(name = options['dataset'])
		except Dataset.DoesNotExist:
			raise CommandError('Dataset %s not found' % options['dataset'])
		
		# Parse the options
		model_name = options['model_name'] or self.get_model_name(dataset)
		resource_name = options['resource_name'] or self.get_resource_name(dataset)
		file_name = options['file_name'] or self.get_file_name(dataset)
		file_mode = 'wt' if options['overwrite'] else 'xt'
		
		# Write the model file
		file_path = settings.BASE_DIR / 'metadata' / 'models' / file_name
		try:
			with open(file_path, file_mode, encoding = 'UTF_8') as file:
				file.write(self.get_model_file(dataset, model_name))
		except Exception as why:
			raise CommandError('Could not write file %s: %s' % (file_path, why)) from why
		else:
			self.log.info('Wrote file %s', file_path)
		
		# Write the resource file
		file_path = settings.BASE_DIR / 'metadata' / 'resources' / file_name
		try:
			with open(file_path, file_mode, encoding = 'UTF_8') as file:
				file.write(self.get_resource_file(dataset, model_name, resource_name))
		except Exception as why:
			raise CommandError('Could not write file %s: %s' % (file_path, why)) from why
		else:
			self.log.info('Wrote file %s', file_path)
		
		# Write the admin file
		file_path = settings.BASE_DIR / 'metadata' / 'admin' / file_name
		try:
			with open(file_path, file_mode, encoding = 'UTF_8') as file:
				file.write(self.get_admin_file(dataset, model_name))
		except Exception as why:
			raise CommandError('Could not write file %s: %s' % (file_path, why)) from why
		else:
			self.log.info('Wrote file %s', file_path)
		
		# Be kind to the admin
		self.log.info(EPILOGUE)
	
	def get_model_file(self, dataset, model_name):
		'''Return the content of the model file'''
		
		# Get the keywords of the dataset in alphabetical order and set the appropriate model_field
		keywords = dataset.keywords.exclude(name__in = ['id', 'oid', 'data_location', 'tags', 'date_beg', 'date_end', 'wavemin', 'wavemax'])
		
		keywords = sorted(keywords, key=lambda x: x.name)
		
		for keyword in keywords:
			keyword.model_field = MODEL_FIELD_MAP[keyword.type]
		
		# Use Django templates to generate the file content
		template = Template(MODEL_FILE_TEMPLATE)
		context = Context({
			'command': self.command_name,
			'dataset': dataset,
			'model_name': model_name,
			'keywords': keywords,
		})
		
		return template.render(context)

	def get_resource_file(self, dataset, model_name, resource_name):
		'''Return the content of the resource file'''
		
		# Use Django templates to generate the file content
		template = Template(RESOURCE_FILE_TEMPLATE)
		context = Context({
			'command': self.command_name,
			'dataset': dataset,
			'model_name': model_name,
			'resource_name': resource_name,
		})
		
		return template.render(context)
	
	def get_admin_file(self, dataset, model_name):
		'''Return the content of the admin file'''
		
		# Use Django templates to generate the file content
		template = Template(ADMIN_FILE_TEMPLATE)
		context = Context({
			'command': self.command_name,
			'dataset': dataset,
			'model_name': model_name,
		})
		
		return template.render(context)
	
	def get_model_name(self, dataset):
		return re.sub(r'[^a-zA-Z0-9]', '', dataset.name.title())
	
	def get_resource_name(self, dataset):
		return 'metadata_' + re.sub(r'\W', '_', dataset.name.lower())
	
	def get_file_name(self, dataset):
		return re.sub(r'\W', '_', dataset.name.lower()) + '.py'
