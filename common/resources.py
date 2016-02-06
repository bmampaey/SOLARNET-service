from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from SDA.resources import ResourceMeta
from common.models import DataLocation, Tag

class TagResource(ModelResource):
	'''RESTful resource for model Tag'''
	# TODO check how to add metadata in detail view ListField?
	# Better add the related fields at run time
	
	class Meta(ResourceMeta):
		queryset = Tag.objects.all()
		resource_name = 'tag'
		filtering = {'name': ALL}


class DataLocationResource(ModelResource):
	'''Resource for DataLocation models'''
	# TODO check how to add metadata in detail view ListField?
	# Better add the related fields at run time
	class Meta(ResourceMeta):
		queryset = DataLocation.objects.all()
		resource_name = 'data_location'


class BaseMetadataResource(ModelResource):
	'''Base resource for Metadata models'''
	
	data_location = fields.ToOneField(DataLocationResource, 'data_location', full=True)
	tags = fields.ToManyField(TagResource, 'tags', full=True)
	
	class Meta(ResourceMeta):
		excludes = ['id']
		detail_uri_name = 'oid'
		filtering = {'tags': ALL_WITH_RELATIONS}
		ordering = []
	
	def __init__(self):
		super(BaseMetadataResource, self).__init__()
		# Add filtering and ordering by all regular fields
		for field in self.Meta.object_class._meta.get_fields():
			if not field.is_relation:
    				self._meta.filtering.setdefault(field.name, ALL)
    				self._meta.ordering.append(field.name)