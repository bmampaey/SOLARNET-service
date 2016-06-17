from django.db.models import Q
from django.conf.urls import url
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.exceptions import InvalidFilterError
from tastypie.utils import trailing_slash
from SDA.resources import ResourceMeta
from dataset.resources import Dataset, DataLocationResource
from metadata.models import Tag, AiaLev1, Chrotel, Eit, HmiMagnetogram, SwapLev1, Themis, Xrt

from .filters import ComplexFilter, ParseException

class TagResource(ModelResource):
	'''RESTful resource for model Tag'''
	# TODO check how to add metadata in detail view ListField?
	# Better add the related fields at run time
	
	class Meta(ResourceMeta):
		queryset = Tag.objects.all()
		resource_name = 'tag'
		max_limit = None
		limit = None
		filtering = {'name': ALL}
	
	def build_filters(self, filters=None, ignore_bad_filters=False):
		# Allow more intuitive tags filtering on dataset using dataset={dateset_id}
		# This filter allows only to get tags for one dataset
		orm_filters = super(TagResource, self).build_filters(filters, ignore_bad_filters)
		if "dataset" in filters:
			try:
				dataset = Dataset.objects.get(id=filters['dataset'])
			except Dataset.DoesNotExist:
				# filter that will always return an empty queryset
				orm_filters['pk__isnull'] = True
			else:
				foreign_key_name = dataset._metadata_model.app_label + '_' + dataset._metadata_model.model 
				orm_filters[foreign_key_name + '__isnull'] = False
		
		return orm_filters
	
	def apply_filters(self, request, applicable_filters):
		# Avoid duplicate results
		return super(TagResource, self).apply_filters(request, applicable_filters).distinct()
	
	def build_schema(self):
		data = super(TagResource, self).build_schema()
		data['filtering']['dataset'] = 'exact'
		return data

class BaseMetadataResource(ModelResource):
	'''Base RESTful resource for Metadata models'''
	
	data_location = fields.ToOneField(DataLocationResource, 'data_location', full=True)
	tags = fields.ToManyField(TagResource, 'tags', full=True, blank=True)
	
	class Meta(ResourceMeta):
		excludes = ['id']
		detail_uri_name = 'oid'
		filtering = {'tags': ALL_WITH_RELATIONS}
		ordering = []
	
	def __init__(self):
		super(BaseMetadataResource, self).__init__()
		# Add filtering and ordering by all regular fields
		if getattr(self._meta, 'object_class', None) is not None:
			for field in self._meta.object_class._meta.get_fields():
				if not field.is_relation and not field.auto_created:
	    				self._meta.filtering.setdefault(field.name, ALL)
	    				self._meta.ordering.append(field.name)
	
	def base_urls(self):
		# Override base urls to group ressources under a common  path
		return [
			url(r"^metadata/(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
			url(r"^metadata/(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash), self.wrap_view('get_schema'), name="api_get_schema"),
			url(r"^metadata/(?P<resource_name>%s)/set/(?P<%s_list>.*?)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash), self.wrap_view('get_multiple'), name="api_get_multiple"),
			url(r"^metadata/(?P<resource_name>%s)/(?P<%s>.*?)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
		]
	
	def build_filters(self, filters=None, ignore_bad_filters=False):
		'''Allow more complex filtering on metadata using search parameter'''
		# Strangely tastypie will pass a querydict or a dict for the filters keyword
		try:
			search_filters = filters.getlist('search', None)
		except AttributeError:
			search_filters = filters.get('search', None)
		
		orm_filters = super(BaseMetadataResource, self).build_filters(filters, ignore_bad_filters)
		
		if search_filters is not None:
			try:
				orm_filters['search'] = reduce(lambda a, b: a & ComplexFilter.parseString(b)[0].as_q(), search_filters, Q())
			except ParseException, why:
				if not ignore_bad_filters:
					raise InvalidFilterError(str(why))
		
		return orm_filters
	
	def apply_filters(self, request, applicable_filters):
		'''Apply complex search filter'''
		#import pdb; pdb.set_trace()
		search_filter = applicable_filters.pop('search', None)
		# if one of the filters is tags__in, then we should add .distinct()
		# but this makes the queries run very slow
		partially_filtered = super(BaseMetadataResource, self).apply_filters(request, applicable_filters)
		if search_filter is not None:
			applicable_filters['search'] = search_filter
			return partially_filtered.filter(search_filter)
		else:
			return partially_filtered
	
	def build_schema(self):
		data = super(BaseMetadataResource, self).build_schema()
		data['filtering']['search'] = 'exact'
		return data

class AiaLev1Resource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = AiaLev1.objects.all()
		resource_name = 'aia_lev1'

class ChrotelResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = Chrotel.objects.all()
		resource_name = 'chrotel'

class EitResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = Eit.objects.all()
		resource_name = 'eit'

class HmiMagnetogramResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = HmiMagnetogram.objects.all()
		resource_name = 'hmi_magnetogram'

class SwapLev1Resource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = SwapLev1.objects.all()
		resource_name = 'swap_lev1'

class ThemisResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = Themis.objects.all()
		resource_name = 'themis'

class XrtResource(BaseMetadataResource):
	
	class Meta(BaseMetadataResource.Meta):
		queryset = Xrt.objects.all()
		resource_name = 'xrt'