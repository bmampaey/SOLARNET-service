from django.test import TestCase
from django.contrib.auth.models import Permission

from dataset.tests.utils import create_test_dataset
from api.tests.mixins import ResourceTestCaseMixin

class TestDataLocationResource(ResourceTestCaseMixin, TestCase):
	'''Test the DataLocationResource'''
	
	resource_name = 'data_location'
	
	def setUp(self):
		super().setUp()
		# Create test data
		self.test_dataset = create_test_dataset()
		self.test_data_location = self.test_dataset.data_locations.create(file_url = 'https://test.com/file.fits', file_size = 1024, file_path = 'test_path/file.fits', offline=True)
		
		self.test_instance = self.test_data_location
		self.test_post_data = {
			'dataset': self.test_dataset,
			'file_url': 'https://test.com/new_file.fits',
			'file_size': 2048,
			'file_path': 'test_path/new_file.fits',
			'offline': True
		}
		self.test_patch_data = {
			'file_url': 'https://test.com/other_file.fits',
			'file_size': 4096,
			'file_path': 'test_path/other_file.fits',
			'offline': False
		}
	
	def test_get_list(self):
		'''Test a GET on the list URL'''
		
		msg = 'When no authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of data locations'
		response = self.api_client.get(self.get_resource_uri(), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, file_url = [self.test_data_location.file_url], msg=msg)
		
		msg = 'When authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of data locations'
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, file_url = [self.test_data_location.file_url], msg=msg)
	
	def test_post_list(self):
		'''Test a POST on the list URL'''
		
		msg = 'When no authentication is provided, a POST must return an unauthorized response'
		data = self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided but user has not permission, a POST must return an unauthorized response'
		data = self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and user has permission, but the user does not belong to the dataset user_group, a POST must return an unauthorized response'
		self.test_user.user_permissions.add(Permission.objects.get(codename='add_datalocation'))
		data = self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and user has permission, and the user belongs to the dataset user_group, a POST must return an OK response and the data location must have been created'
		self.test_user.groups.add(self.test_dataset.user_group)
		data = self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpCreated(response, msg=msg)
		self.assertObjectCreated(self.test_dataset.data_locations, file_url = data['file_url'], file_size = data['file_size'], msg=msg)
	
	def test_get_detail(self):
		'''Test a GET on the detail URL'''
		
		msg = 'When no authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_data_location), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['dataset', 'file_url', 'file_size', 'file_path', 'thumbnail_url', 'update_time', 'offline'], msg=msg)
		
		msg = 'When authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_data_location), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['dataset', 'file_url', 'file_size', 'file_path', 'thumbnail_url', 'update_time', 'offline'], msg=msg)
		
	def test_patch_detail(self):
		'''Test a PATCH on the detail URL'''
		
		msg = 'When no authentication is provided, a PATCH must return an unauthorized response'
		data = self.get_test_patch_data()
		response = self.api_client.patch(self.get_resource_uri(self.test_data_location), data=data, format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided but user has not permission, a PATCH must return an unauthorized response'
		data = self.get_test_patch_data()
		response = self.api_client.patch(self.get_resource_uri(self.test_data_location), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and user has permission, but the user does not belong to the dataset user_group, a PATCH must return an unauthorized response'
		self.test_user.user_permissions.add(Permission.objects.get(codename='change_datalocation'))
		data = self.get_test_patch_data()
		response = self.api_client.patch(self.get_resource_uri(self.test_data_location), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and user has permission, and the user belong to the dataset user_group, a PATCH must return an OK response and the data location must have been updated'
		self.test_user.groups.add(self.test_dataset.user_group)
		data = self.get_test_patch_data()
		response = self.api_client.patch(self.get_resource_uri(self.test_data_location), data=data, format='json', authentication=self.test_user_authentication)
		self.test_data_location.refresh_from_db()
		self.assertHttpAccepted(response, msg=msg)
		self.assertAttributesEqual(self.test_data_location, data, msg=msg)
	
	def test_delete_detail(self):
		'''Test a DELETE on the detail URL'''
		
		msg = 'When no authentication is provided, a DELETE must return an unauthorized response'
		response = self.api_client.delete(self.get_resource_uri(self.test_data_location), format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided but user has not permission, a DELETE must return an unauthorized response'
		response = self.api_client.delete(self.get_resource_uri(self.test_data_location), format='json', authentication=self.test_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and user has permission, but the user does not belong to the dataset user_group, a DELETE must return an unauthorized response'
		self.test_user.user_permissions.add(Permission.objects.get(codename='delete_datalocation'))
		response = self.api_client.delete(self.get_resource_uri(self.test_data_location), format='json', authentication=self.test_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and user has permission, and the user belong to the dataset user_group, a DELETE must return an empty response and the data location must have been deleted'
		self.test_user.groups.add(self.test_dataset.user_group)
		response = self.api_client.delete(self.get_resource_uri(self.test_data_location), format='json', authentication=self.test_user_authentication)
		self.assertHttpAccepted(response, msg=msg)
		self.assertObjectDeleted(self.test_data_location, msg=msg)
	
	def test_validation_errors(self):
		'''Test that creating data location with invalid data return appropriate error messages'''
		
		# Give user permission to create/update
		self.test_user.groups.add(self.test_dataset.user_group)
		self.test_user.user_permissions.add(Permission.objects.get(codename='add_datalocation'))
		self.test_user.user_permissions.add(Permission.objects.get(codename='change_datalocation'))
		
		msg = 'When file_url is not a proper URL, a POST must return a bad request with a proper error message'
		data = self.get_test_post_data(file_url = 'not a proper URL')
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpBadRequest(response, msg=msg)
		self.assertIn('file_url', response.content.decode(response.charset), msg=msg)
		
		msg = 'When file_size is not a positive integer, a POST must return a bad request with a proper error message'
		data = self.get_test_post_data(file_size = -1)
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpBadRequest(response, msg=msg)
		self.assertIn('file_size', response.content.decode(response.charset), msg=msg)
		
		msg = 'When file_path is not an accepted path, a POST must return a bad request with a proper error message'
		for file_path in [r'/unix/absolute', r'c:\\windows\absolute']:
			with self.subTest(file_path = file_path):
				data = self.get_test_post_data(file_path = file_path)
				response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
				self.assertHttpBadRequest(response, msg=msg)
				self.assertIn('file_path', response.content.decode(response.charset), msg=msg)
		
		msg = 'When thumbnail_url is not a proper URL, a POST must return a bad request with a proper error message'
		data = self.get_test_post_data(thumbnail_url = 'not a proper URL')
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpBadRequest(response, msg=msg)
		self.assertIn('thumbnail_url', response.content.decode(response.charset), msg=msg)
		
		msg = 'When offline is not a accepted boolean value, a POST must return a bad request with a proper error message'
		data = self.get_test_post_data(offline = 'true')
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpBadRequest(response, msg=msg)
		self.assertIn('offline', response.content.decode(response.charset), msg=msg)
		
		msg = 'When a data location with the same dataset and file_url already exists, a POST must return a bad request with a proper error message'
		data = self.get_test_post_data(file_url = self.test_data_location.file_url)
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpBadRequest(response, msg=msg)
		self.assertIn('__all__', response.content.decode(response.charset), msg=msg)
		
		msg = 'When a data location with the same dataset and file_path already exists, a POST must return a bad request with a proper error message'
		data = self.get_test_post_data(file_path = self.test_data_location.file_path)
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpBadRequest(response, msg=msg)
		self.assertIn('__all__', response.content.decode(response.charset), msg=msg)
