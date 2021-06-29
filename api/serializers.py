from tastypie.serializers import Serializer as BaseSerializer
from django.core.serializers.json import DjangoJSONEncoder
from simplejson import dumps

__all__ = ['Serializer']

class Serializer(BaseSerializer):
	'''Serializer that redefines date and time formating to enfore timezone and json serializing to remove NaN and Infinity'''
	
	def format_datetime(self, data):
		'''Formate datetime using iso-8601 with timezone and without microseconds'''
		# If the timezone is UTC (+00:00) replace it by Z for easier display
		return data.isoformat(timespec = 'milliseconds').replace('+00:00', 'Z')
	
	def format_date(self, data):
		'''Formate date using iso-8601'''
		return data.isoformat()
	
	def format_time(self, data):
		'''Formate time using iso-8601 with timezone and without microseconds'''
		# If the timezone is UTC (+00:00) replace it by Z for easier display
		return data.isoformat(timespec = 'milliseconds').replace('+00:00', 'Z')
	
	def to_json(self, data, options=None):
		'''Given some Python data, produces JSON output compliant to ECMA script'''
		data = self.to_simple(data, options)
		# Override to use a JSON encoder that encode NaN and Inf values to null
		return dumps(data, ensure_ascii=False, ignore_nan=True, default=DjangoJSONEncoder.default)
