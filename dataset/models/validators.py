from keyword import iskeyword
from pathlib import PurePosixPath, PureWindowsPath
from django.core.exceptions import ValidationError
from django.conf import settings

__all__ = ['valid_keyword_name', 'valid_file_path']

def valid_keyword_name(value):
	'''Check that the keyword name can be used as a django model field name'''
	
	# Check that the name is a valid python identifier
	if not value.isidentifier():
		raise ValidationError('%(value)s is not a valid python identifier', params={'value': value}, code='invalid')
	
	# Check that the name is not a reserved keyword
	if iskeyword(value):
		raise ValidationError('%(value)s is a reserved python keyword', params={'value': value}, code='invalid')
 	
	# Check that the name does not start with an undescore
	if value.startswith('_'):
		raise ValidationError('keyword name must not start with an undescore', code='invalid')
	
	# Check that the name does not end with an undescore
	if value.endswith('_'):
		raise ValidationError('keyword name must not end with an undescore', code='invalid')
	
	# Check that the name does not contain 2 or more successive undescores
	if '__' in value:
		raise ValidationError('keyword name must not contain 2 successive undescores', code='invalid')


def valid_file_path(value):
	'''Check that the data location file_path is safe for Posix and Windows'''
	posix_path = PurePosixPath(value)
	window_path = PureWindowsPath(value)
	
	if value.endswith('/'):
		raise ValidationError('file path cannot end with a /', code='invalid')
	
	if posix_path.anchor or window_path.anchor:
		raise ValidationError('file path must be a relative path', code='invalid')
	
	if posix_path.is_reserved() or window_path.is_reserved():
		raise ValidationError('%(value)s is a reserved file path', params={'value': value}, code='invalid')
	
	for character, name in settings.FILE_PATH_FORBIDDEN_CHARACTERS.items():
		if character in value:
				raise ValidationError('%(name)s is a discouraged character in file paths', params={'name': name}, code='invalid')
