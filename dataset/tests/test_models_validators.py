from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from dataset.models.validators import valid_keyword_name, valid_file_path

class TestValidKeywordName(SimpleTestCase):
	'''Test the valid_keyword_name function'''
	
	def test_valid(self):
		'''Test that if the value is a valid django model field identifier, the function does not raises a ValidationError'''
		
		msg = '"%s" is a valid django model field identifier'
		for value in ['hello', 'hello_world', 'he110_w0r1d']:
			self.assertIsNone(valid_keyword_name(value), msg = msg % value)
	
	def test_isidentifier(self):
		'''Test that if the value is not a valid python identifier, the function raises a ValidationError'''
		
		msg = '"%s" is not a valid python identifier'
		for value in ['should not contain spaces', '0shouldnotstartwith0', 'should-not-have-dash']:
			with self.assertRaises(ValidationError, msg = msg % value):
				valid_keyword_name(value)
	
	def test_iskeyword(self):
		'''Test that if the value is not python reserved keyword, the function raises a ValidationError'''
		
		msg = '"%s" is a python reserved keyword'
		for value in ['global', 'class', 'continue', 'pass']:
			with self.assertRaises(ValidationError, msg = msg % value):
				valid_keyword_name(value)
	
	def test_undescores(self):
		'''Test that if the value starts with an underscore or has 2 or more consecutive undescores, the function raises a ValidationError'''
		
		msg = '"%s" has unacceptable undescores'
		for value in ['_', '_a', '__a', 'a_', 'a__', 'a__b', 'a___b']:
			with self.assertRaises(ValidationError, msg = msg % value):
				valid_keyword_name(value)


class TestValidFilePath(SimpleTestCase):
	'''Test the valid_file_path function'''
	
	def test_valid(self):
		'''Test that if the value is a valid file path, the function does not raises a ValidationError'''
		
		msg = '"%s" is a valid file path'
		for value in ['file.fits', 'test_path/file.fits', 'test_path/sub_path/file.fits', 'file name.fits', 'FILE.FITS']:
			self.assertIsNone(valid_file_path(value), msg = msg % value)
	
	def test_relative_file_path(self):
		'''Test that if the value is not a relative file path, the function raises a ValidationError'''
		
		msg = '"%s" is not a relative file path'
		for value in [r'/unix/absolute', r'c:\\windows\absolute', r'/absolute/directory/path/', r'relative/directory/path/']:
			with self.assertRaises(ValidationError, msg = msg % value):
				valid_file_path(value)
	
	def test_reserved(self):
		'''Test that if the value is a reserved windows path, the function raises a ValidationError'''
		
		msg = '"%s" is a windows reserved path'
		value = 'nul'
		with self.assertRaises(ValidationError, msg = msg % value):
			valid_file_path(value)
	
	def test_forbidden_character(self):
		'''Test that if the value contains one of the forbidden character, the function raises a ValidationError'''
		
		msg = '"%s" contains a forbidden character'
		for value in [r'test_path\file.fits', 'file*.fits', '| grep', 'file.fits\n']:
			with self.assertRaises(ValidationError, msg = msg % value):
				valid_file_path(value)
