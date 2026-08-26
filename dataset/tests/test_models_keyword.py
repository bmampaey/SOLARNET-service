import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from dataset.models import KeywordType
from dataset.tests.utils import create_test_dataset


class TestKeywordModel(TestCase):
	"""Test the Keyword model"""

	def setUp(self):
		super().setUp()
		# Create a test dataset for the keywords
		self.test_dataset = create_test_dataset()
		self.test_keyword = self.test_dataset.keywords.create(
			name='test',
			verbose_name='Test',
			type=KeywordType.TEXT,
			description='A test keyword',
			constant_value=None,
		)

	def test_converted_constant_value(self):
		"""Test the converted_constant_value property"""

		msg = 'When the constant_value is None, the method return None'
		self.test_keyword.constant_value = None
		self.assertIsNone(self.test_keyword.converted_constant_value, msg=msg)

		msg = 'When the keyword type is TEXT, the method return a str'
		self.test_keyword.constant_value = 'some text'
		self.test_keyword.type = KeywordType.TEXT
		self.assertIsInstance(self.test_keyword.converted_constant_value, str, msg=msg)

		msg = 'When the keyword type is BOOLEAN, the method return a bool'
		self.test_keyword.constant_value = 'true'
		self.test_keyword.type = KeywordType.BOOLEAN
		self.assertIsInstance(self.test_keyword.converted_constant_value, bool, msg=msg)

		msg = 'When the keyword type is INTEGER, the method return a int'
		self.test_keyword.constant_value = '1'
		self.test_keyword.type = KeywordType.INTEGER
		self.assertIsInstance(self.test_keyword.converted_constant_value, int, msg=msg)

		msg = 'When the keyword type is REAL, the method return a float'
		self.test_keyword.constant_value = '1'
		self.test_keyword.type = KeywordType.REAL
		self.assertIsInstance(self.test_keyword.converted_constant_value, float, msg=msg)

		msg = 'When the keyword type is TIME_ISO_8601, the method return a datetime.datetime'
		self.test_keyword.constant_value = '2000-01-01T00:00:00'
		self.test_keyword.type = KeywordType.TIME_ISO_8601
		self.assertIsInstance(self.test_keyword.converted_constant_value, datetime.datetime, msg=msg)

		msg = 'When the constant_value cannot be converted to the keyword type, the method raises a ValueError'
		# Boolean only accept "true" or "false"
		self.test_keyword.constant_value = '1'
		self.test_keyword.type = KeywordType.BOOLEAN
		with self.assertRaises(ValueError, msg=msg):
			self.test_keyword.converted_constant_value

	def test_clean(self):
		"""Test the clean method"""

		msg = 'When the constant_value can be converted to the keyword type, the method does not raises a ValidationError'
		# Boolean only accept "true" or "false"
		self.test_keyword.constant_value = 'true'
		self.test_keyword.type = KeywordType.BOOLEAN
		self.test_keyword.clean()

		msg = 'When the constant_value cannot be converted to the keyword type, the method raises a ValidationError'
		# Boolean only accept "true" or "false"
		self.test_keyword.constant_value = '1'
		self.test_keyword.type = KeywordType.BOOLEAN
		with self.assertRaises(ValidationError, msg=msg):
			self.test_keyword.clean()
