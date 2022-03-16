from django.test import TestCase
from django.contrib.auth.models import User

from api.tests.mixins import ResourceTestCaseMixin
from dataset.tests.utils import create_test_dataset

class TestDataSelectionResource(ResourceTestCaseMixin, TestCase):
	'''Test the DataSelectionResource'''
	
	resource_name = 'data_selection'
	
	def setUp(self):
		super().setUp()
		# Create test data
		self.test_dataset = create_test_dataset()
		self.test_metadata1 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata1')
		self.test_metadata2 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata2')
		self.test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset, description='test data selection')
		# Create another user to check that it's data selections are not accessible by our test user
		self.other_user = User.objects.create_user(username='other_test@test.com', email='other_test@test.com', password='test', first_name='test', last_name='test')
		self.other_user_authentication = self.get_authentication(self.other_user, password = 'test')
		self.other_test_data_selection = self.other_user.data_selections.create(dataset = self.test_dataset, description = 'other user test data selection')
		
		self.test_instance = self.test_data_selection
		self.test_post_data = {
			'dataset': self.test_dataset,
			'query_string': 'oid=test_metadata2',
			'description': 'new test data selection'
		}
		self.test_patch_data = {
			'query_string': 'oid=test_metadata1',
			'description': 'other description'
		}
	
	def test_get_list(self):
		'''Test a GET on the list URL'''
		
		msg = 'When no authentication is provided, a GET on the list URL must return an unauthorized response'
		response = self.api_client.get(self.get_resource_uri(), format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of data selection owned by the user'
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, description = [self.test_data_selection.description], msg=msg)
	
	def test_post_list(self):
		'''Test a POST on the list URL'''
		
		msg = 'When no authentication is provided, a POST on the list URL must return an unauthorized response'
		response = self.api_client.post(self.get_resource_uri(), format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided, a POST must return an OK response and the data selection must have been created'
		data = self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpCreated(response, msg=msg)
		self.assertObjectCreated(self.test_user.data_selections, description = data['description'], msg=msg)
	
	def test_get_detail(self):
		'''Test a GET on the detail URL'''
		
		msg = 'When no authentication is provided, a GET on the detail URL must return an unauthorized response'
		response = self.api_client.get(self.get_resource_uri(self.test_data_selection), format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and the owner is not the user, a GET on the detail URL must return an unauthorized response'
		response = self.api_client.get(self.get_resource_uri(self.test_data_selection), format='json', authentication=self.other_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and the owner is the user, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_data_selection), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['dataset', 'query_string', 'description', 'creation_time', 'zip_download_url', 'ftp_download_url', 'metadata'], msg=msg)
	
	def test_get_detail_metadata(self):
		'''Test the metadata field for a GET on the detail URL'''
		
		msg = 'When no query_string is specified, the metadata field resource_uri must be exactly the metadata ressource list url'
		response = self.api_client.get(self.get_resource_uri(self.test_data_selection), format='json', authentication=self.test_user_authentication)
		self.assertGetDetailResponseContains(response, metadata = {'resource_uri': self.get_resource_uri(resource_name='base_metadata_test_resource'), 'count': 2}, msg=msg)
		
		msg = 'When a query_string is specified, the metadata field resource_uri must include the query_string'
		self.test_data_selection.query_string = 'oid=test_metadata1'
		self.test_data_selection.save()
		response = self.api_client.get(self.get_resource_uri(self.test_data_selection), format='json', authentication=self.test_user_authentication)
		self.assertGetDetailResponseContains(response, metadata = {'resource_uri': self.get_resource_uri(resource_name='base_metadata_test_resource') + '?oid=test_metadata1', 'count': 1}, msg=msg)
	
	def test_patch_detail(self):
		'''Test a PATCH on the detail URL'''
		
		msg = 'When no authentication is provided, a PATCH on the detail URL must return an unauthorized response'
		response = self.api_client.patch(self.get_resource_uri(self.test_data_selection), format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and the owner is not the user, a PATCH must return an unauthorized response'
		data = self.get_test_patch_data()
		response = self.api_client.patch(self.get_resource_uri(self.test_data_selection), data=data, format='json', authentication=self.other_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and the owner is the user, a PATCH must return an OK response and the data selection must have been updated'
		data = self.get_test_patch_data()
		response = self.api_client.patch(self.get_resource_uri(self.test_data_selection), data=data, format='json', authentication=self.test_user_authentication)
		self.test_data_selection.refresh_from_db()
		self.assertHttpAccepted(response, msg=msg)
		self.assertAttributesEqual(self.test_data_selection, data, msg=msg)
	
	def test_delete_detail(self):
		'''Test a DELETE on the detail URL'''
		
		msg = 'When no authentication is provided, a DELETE on the detail URL must return an unauthorized response'
		response = self.api_client.delete(self.get_resource_uri(self.test_data_selection), format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and the owner is not the user, a DELETE must return an unauthorized response'
		response = self.api_client.delete(self.get_resource_uri(self.test_data_selection), format='json', authentication=self.other_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and the owner is the user, a DELETE must return an empty response and the data selection must have been deleted'
		response = self.api_client.delete(self.get_resource_uri(self.test_data_selection), format='json', authentication=self.test_user_authentication)
		self.assertHttpAccepted(response, msg=msg)
		self.assertObjectDeleted(self.test_data_selection, msg=msg)
	
	def test_validation_errors(self):
		'''Test that creating/updating data selection with invalid data return appropriate error messages'''
		# There is no validator or unique constraint in DataSelection
		pass
