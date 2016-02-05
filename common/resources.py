from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from SDA.resources import ResourceMeta
from common.models import DataLocation, Tag

class TagResource(ModelResource):
	'''RESTful resource for model Tag'''
	class Meta(ResourceMeta):
		queryset = Tag.objects.all()
		resource_name = 'tag'
		filtering = {"name": ALL}



class DataLocationResource(ModelResource):
# TODO now a one to many
#	metadata = fields.OneToOneField(dataset_name+'.resources.MetadaResource', 'metadata', related_name='data_location', null=True, blank=True)

	class Meta(ResourceMeta):
		queryset = DataLocation.objects.all()
		resource_name = 'data_location'


class BaseMetadaResource(ModelResource):
	'''Base resource for Metadata models'''
	data_location = fields.OneToOneField(DataLocationResource, 'data_location', related_name='metadata', full=True, null=True, blank=True)
	tags = fields.ToManyField(TagResource, 'tags', full=True)
	
	class Meta(ResourceMeta):
		filtering = {"tags": ALL_WITH_RELATIONS}
		ordering = []
	
	def __init__(self):
		super(BaseMetadaResource, self).__init__()
		# Add filtering and ordering by all regular fields
		for field in self.Meta.object_class._meta.get_fields():
			if not field.is_relation:
    				self.Meta.filtering.setdefault(field.name, ALL)
    				self.Meta.ordering.append(field.name)