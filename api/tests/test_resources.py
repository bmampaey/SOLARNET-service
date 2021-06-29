from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .mixins import SvoApiTestCaseMixin

# Use a TransactionTestCase because we will provoke an IntegrityError that would break a TestCase
class TestUserResource(SvoApiTestCaseMixin, TransactionTestCase):
	'''Test the UserResource'''
	
	resource_name = 'user'
	
	def test_get_list(self):
		'''Test a GET on the list URL'''
		
		msg = 'When no authentication is provided, a GET on the list URL must return an unauthorized response'
		response = self.api_client.get(self.get_resource_uri(), format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When the user does not exists, even if authentication is provided, a GET on the list URL must return an unauthorized response'
		authentication = self.get_basic_authentication('non_existing_user@test.com', 'test')
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When the user exists, but incorrect authentication is provided, a GET on the list URL must return an unauthorized response'
		authentication = self.get_basic_authentication(self.test_user.username, 'wrong password')
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When the user exists, and correct authentication is provided, a GET on the list URL must return a valid JSON response with the name and api_key'
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertDictEqual(self.deserialize(response), {'name': self.test_user.get_full_name(), 'api_key': self.test_user.api_key.key}, msg=msg)
	
	def test_post_list(self):
		'''Test a POST on the list URL'''
		
		msg = 'When a valid email is provided but the user exists already, a POST on the list URL must return a bad request response'
		data = {
			'email': self.test_user.email,
			'first_name': self.test_user.first_name,
			'last_name': self.test_user.last_name,
			'password': 'test'
		}
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json')
		self.assertHttpBadRequest(response, msg=msg)
		
		msg = 'When a invalid email is provided, a POST on the list URL must return a bad request response'
		data['email'] = 'not a vaild email'
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json')
		self.assertHttpBadRequest(response, msg=msg)
		
		msg = 'When a valid email is provided, and the user does not yet exist, a POST on the list URL must return a created response with the name and api_key'
		data['email'] = 'other_test@test.com'
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json')
		self.assertHttpCreated(response, msg=msg)
		user = User.objects.get(username=data['email'])
		self.assertDictEqual(self.deserialize(response), {'name': user.get_full_name(), 'api_key': user.api_key.key}, msg=msg)
	
	def test_patch_list(self):
		'''Test a PATCH on the list URL'''
		
		data = {'password': 'new password'}
		
		msg = 'When no authentication is provided, a PATCH on the list URL must return an unauthorized response'
		response = self.api_client.patch(self.get_resource_uri(), data=data, format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When the user does not exists, even if authentication is provided, a PATCH on the list URL must return an unauthorized response'
		authentication = self.get_basic_authentication('non_existing_user@test.com', 'test')
		response = self.api_client.patch(self.get_resource_uri(), data=data, format='json', authentication=authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When the user exists, but incorrect authentication is provided, a PATCH on the list URL must return an unauthorized response'
		authentication = self.get_basic_authentication(self.test_user.username, 'wrong password')
		response = self.api_client.patch(self.get_resource_uri(), data=data, format='json', authentication=authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When the user exists, and correct authentication is provided, a PATCH on the list URL must return a valid JSON response with the name and a new api_key, and the password must have been updated'
		original_api_key = self.test_user.api_key.key
		response = self.api_client.patch(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.test_user.refresh_from_db()
		self.assertValidJSONResponse(response, msg=msg)
		self.assertDictEqual(self.deserialize(response), {'name': self.test_user.get_full_name(), 'api_key': self.test_user.api_key.key}, msg=msg)
		self.assertNotEqual(original_api_key, self.test_user.api_key.key, msg=msg)
		self.assertIsNotNone(authenticate(username=self.test_user.username, password=data['password']), msg=msg)
	
	def test_delete_list(self):
		'''Test a DELETE on the list URL'''
		msg = 'When no authentication is provided, a DELETE on the list URL must return an unauthorized response'
		response = self.api_client.delete(self.get_resource_uri(), format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When the user does not exists, even if authentication is provided, a DELETE on the list URL must return an unauthorized response'
		authentication = self.get_basic_authentication('non_existing_user@test.com', 'test')
		response = self.api_client.delete(self.get_resource_uri(), format='json', authentication=authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When the user exists, but incorrect authentication is provided, a DELETE on the list URL must return an unauthorized response'
		authentication = self.get_basic_authentication(self.test_user.username, 'wrong password')
		response = self.api_client.delete(self.get_resource_uri(), format='json', authentication=authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When the user exists, and correct authentication is provided, a DELETE on the list URL must return an empty response and the user must have been deleted'
		response = self.api_client.delete(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertHttpAccepted(response, msg=msg)
		self.assertObjectDeleted(self.test_user, msg=msg)
	
	def test_put_list(self):
		'''Test a PUT on the list URL'''
		
		msg = 'A PUT on the list URL must return a not allowed response'
		data = {'password': 'new password'}
		response = self.api_client.put(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpMethodNotAllowed(response, msg=msg)
	
	def test_get_schema(self):
		'''Test a GET on the schema URL'''
		
		msg = 'A GET on the schema URL must return a valid JSON response with the allowed_list_http_methods'
		response = self.api_client.get(self.resource.get_resource_uri(url_name='api_get_schema'), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetDetailResponseContains(response, allowed_list_http_methods = ['post', 'get', 'patch', 'delete'], msg=msg)
	
	def test_detail_view(self):
		'''Test that the dispatch_detail view is not accessible for the user resource'''
		
		msg = 'The resource URI of a user object must be empty (i.e. there is no reverse match for the detail view)'
		self.assertEqual(self.get_resource_uri(self.test_user), '', msg=msg)
