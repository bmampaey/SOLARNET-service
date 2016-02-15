import os
from django.core.management.commands.startapp import Command as StartAppCommand
from django.core.management.base import CommandError
from ..logger import Logger


file_templates = {

'models.py': '''
from __future__ import unicode_literals
from django.db import models
from dataset.models import BaseMetadata

class Metadata(BaseMetadata):
	pass
''',

'admin.py' : '''
from django.contrib import admin

from .models import Metadata
from dataset.admin import BaseMetadataAdmin

@admin.register(Metadata)
class MetadataAdmin(BaseMetadataAdmin):
	pass
''',

'serializers.py' : '''
from rest_framework import serializers

from .models import Metadata
from dataset.serializers import DataLocationSerializer

class MetadataSerializer(serializers.HyperlinkedModelSerializer):
	data_location = DataLocationSerializer()
	class Meta:
		model = Metadata
		extra_kwargs = {'uri': {'lookup_field': 'oid'}}
''',

'views.py' : '''
from rest_framework import viewsets

from .models import Metadata
from .serializers import MetadataSerializer

class MetadataViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Metadata.objects.all()
	serializer_class = MetadataSerializer
	lookup_field = 'oid'
'''
}

class Command(StartAppCommand):
	help = 'Start a dataset app and prefill the app files'
	
	def handle(self, **options):
		
		# Parse options
		app_name = options['name']
		target = options['directory']
		
		# Create the app
		#super(Command, self).handle(**options)
		
		# Get the directory where to write files
		# Copied from django/core/management/templates.py
		if target is None:
			top_dir = os.path.join(os.getcwd(), app_name)
		else:
			top_dir = os.path.abspath(os.path.expanduser(target))
		import pdb; pdb.set_trace()
		# Write the files template
		for file_name, template in file_templates.iteritems():
			file_path = os.path.join(top_dir, file_name)
			try:
				with open(file_path, 'w') as f:
					f.write(template)
			except Exception, why:
				raise CommandError('Error writing to file %s: %s' % (file_path, why))
		
		# Remind admin of next steps
		log = Logger(self)
		log.info('DO NOT FORGET:')
		log.info('\t1.Add the app "%s" to the INSTALLED_APPS in the settings file', app_name)
		log.info('\t2.Add the dataset "%s" to the dataset table via the admin interface', app_name)