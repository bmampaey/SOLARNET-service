from tastypie import serializers
from django.core.serializers.json import DjangoJSONEncoder
import simplejson

class Serializer(serializers.Serializer):
	'''Serializer that redefines to_json to convert NaN/Inf to "null"'''
	# add jsonp to the list of allowed format
	formats = serializers.Serializer.formats + ['jsonp']
	
	def to_json(self, data, options=None):
		'''Mixes simplejson dump and django json encoder'''
		options = options or {}
		data = self.to_simple(data, options)
		
		return simplejson.dumps(data, ensure_ascii=False, ignore_nan=True, default=DjangoJSONEncoder.default)