from datetime import datetime, time, date, timedelta, timezone
from django.test import SimpleTestCase
from api.serializers import Serializer

class TestSerializer(SimpleTestCase):
	'''Test the Serializer class'''
	
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.serializer = Serializer()
	
	def test_format_datetime(self):
		'''Test the format_datetime method'''
		
		msg = 'Timezone naive datetime are encoded using ISO 8601 format with microseconds and without timezone'
		value = datetime(2000, 1, 1, 1, 1, 1, 111111)
		self.assertEqual(self.serializer.format_datetime(value), '2000-01-01T01:01:01.111', msg = msg)
		
		msg = 'Timezone aware datetime in UTC are encoded using ISO 8601 format with microseconds and ending with Z'
		value = datetime(2000, 1, 1, 1, 1, 1, 111111, tzinfo = timezone.utc)
		self.assertEqual(self.serializer.format_datetime(value), '2000-01-01T01:01:01.111Z', msg = msg)
		
		msg = 'Timezone aware datetime non UTC are encoded using ISO 8601 format with microseconds and ending with +xx:xx'
		value = datetime(2000, 1, 1, 1, 1, 1, 111111, tzinfo = timezone(timedelta(hours=1)))
		self.assertEqual(self.serializer.format_datetime(value), '2000-01-01T01:01:01.111+01:00', msg = msg)
	
	def test_format_date(self):
		'''Test the format_date method'''
		
		msg = 'Date are encoded using ISO 8601 format'
		value = date(2000, 1, 1)
		self.assertEqual(self.serializer.format_date(value), '2000-01-01', msg = msg)
	
	def test_format_time(self):
		'''Test the format_time method'''
		
		msg = 'Timezone naive time are encoded using ISO 8601 format with microseconds and without timezone'
		value = time(1, 1, 1, 111111)
		self.assertEqual(self.serializer.format_time(value), '01:01:01.111', msg = msg)
		
		msg = 'Timezone aware time in UTC are encoded using ISO 8601 format with microseconds and ending with Z'
		value = time(1, 1, 1, 111111, tzinfo = timezone.utc)
		self.assertEqual(self.serializer.format_time(value), '01:01:01.111Z', msg = msg)
		
		msg = 'Timezone aware time non UTC are encoded using ISO 8601 format with microseconds and ending with +xx:xx'
		value = time(1, 1, 1, 111111, tzinfo = timezone(timedelta(hours=1)))
		self.assertEqual(self.serializer.format_time(value), '01:01:01.111+01:00', msg = msg)
	
	def test_to_json(self):
		'''Test the to_json method'''
		
		msg = 'NaN, Inf and -Inf must be encoded as "null" for json, other objects are encoded as usual'
		data = [float('NaN'), float('Inf'), float('-Inf'), 1]
		self.assertEqual(self.serializer.to_json(data), '[null, null, null, 1]', msg = msg)
