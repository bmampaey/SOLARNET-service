from base64 import b64encode
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from tastypie.test import TestApiClient
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication

from api import svo_api
from api.serializers import Serializer

__all__ = ['SvoApiTestCaseMixin', 'ResourceTestCaseMixin', 'ReadOnlyResourceTestCaseMixin']

class TestSerializer(Serializer):
	'''A serializer that converts model instances to URI'''
	
	def to_simple(self, data, options):
		if isinstance(data, Model):
			resource = svo_api.canonical_resource_for(type(data))
			return resource.get_resource_uri(data)
		else:
			return super().to_simple(data, options)

# A copy of the tastypie ResourceTestCaseMixin but with some errors fixed
class SvoApiTestCaseMixin:
	'''A mixin of useful methods for testing the SVO API, to be used with Django's TestCase and TransactionTestCase classes'''
	
	# Must override resource
	resource_name = None
	
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.resource = svo_api.canonical_resource_for(cls.resource_name)
		cls.serializer = TestSerializer()
		cls.api_client = TestApiClient(serializer = cls.serializer)
	
	def setUp(self):
		super().setUp()
		# Create a test user and it's authentication for use in the api_client
		self.test_user = User.objects.create_user(username='test@test.com', email='test@test.com', password='test', first_name='test', last_name='test')
		self.test_user_authentication = self.get_authentication(self.test_user, password = 'test')
	
	def get_authentication(self, user, password):
		'''Returns the HTTP Authorization header for use with the resource'''
		if isinstance(self.resource._meta.authentication, ApiKeyAuthentication):
			return self.get_apikey_authentication(user.username, user.api_key.key)
		elif isinstance(self.resource._meta.authentication, BasicAuthentication):
			return self.get_basic_authentication(user.username, password)
		else:
			raise NotImplementedError('You must override get_authentication for authentication class %s' % self.resource._meta.authentication.__class__.__name__)
	
	def get_basic_authentication(self, username, password):
		'''Returns the HTTP Authorization header for use with BasicAuthentication'''
		return 'Basic %s' % b64encode(':'.join([username, password]).encode('utf-8')).decode('utf-8')
	
	def get_apikey_authentication(self, username, api_key):
		'''Returns the HTTP Authorization header for use with ApiKeyAuthentication'''
		return 'ApiKey %s:%s' % (username, api_key)
	
	def get_resource_uri(self, obj = None, resource_name = None):
		'''Returns a URI for the resource'''
		if resource_name is None:
			resource = self.resource
		else:
			resource = svo_api.canonical_resource_for(resource_name)
		# Django reverse quotes the returned URL which breaks the tests if there is a space in the URL
		return resource.get_resource_uri(obj)
	
	def deserialize(self, response):
		'''Deserialize the response content following the "Content-Type" header value and return a Python datastructure'''
		return self.serializer.deserialize(response.content, format=response['Content-Type'])
	
	def serialize(self, data, format='application/json'):
		'''Serialize a Python datastructure to the required format'''
		return self.serializer.serialize(data, format=format)
	
	def assertHttpOK(self, resp, msg = None):
		'''Ensures the response has an HTTP status code of 200'''
		return self.assertEqual(resp.status_code, 200, msg=msg)
	
	def assertHttpCreated(self, resp, msg = None):
		'''Ensures the response has an HTTP status code of 201'''
		return self.assertEqual(resp.status_code, 201, msg=msg)
	
	def assertHttpAccepted(self, resp, msg = None):
		'''Ensures the response is returning either a HTTP 202 or a HTTP 204'''
		self.assertIn(resp.status_code, [202, 204], msg=msg)
	
	def assertHttpBadRequest(self, resp, msg = None):
		'''Ensures the response has an HTTP status code of 400'''
		return self.assertEqual(resp.status_code, 400, msg=msg)
	
	def assertHttpUnauthorized(self, resp, msg = None):
		'''Ensures the response has an HTTP status code of 401'''
		return self.assertEqual(resp.status_code, 401, msg=msg)
	
	def assertHttpForbidden(self, resp, msg = None):
		'''Ensures the response has an HTTP status code of 403'''
		return self.assertEqual(resp.status_code, 403, msg=msg)
	
	def assertHttpNotFound(self, resp, msg = None):
		'''Ensures the response has an HTTP status code of 404'''
		return self.assertEqual(resp.status_code, 404, msg=msg)
	
	def assertHttpMethodNotAllowed(self, resp, msg = None):
		'''Ensures the response has an HTTP status code of 405'''
		return self.assertEqual(resp.status_code, 405, msg=msg)
	
	def assertHttpApplicationError(self, resp, msg = None):
		'''Ensures the response has an HTTP status code of 500'''
		return self.assertEqual(resp.status_code, 500, msg=msg)
	
	def assertValidJSON(self, data, msg = None):
		'''Ensures that the data is a valid JSON string'''
		# Just try the load, if it fails it will throw an exception
		try:
			self.serializer.from_json(data)
		except Exception as why:
			msg = self._formatMessage(msg, '%s is not valid JSON (%s)' % (data, why))
			raise self.failureException(msg)
	
	def assertValidJSONResponse(self, response, msg = None):
		'''Ensures that the HttpResponse:
		* has an HTTP status code of 200
		* has a correct "Content-Type" header (i.e. "application/json")
		* has a content that is valid JSON string
		'''
		self.assertHttpOK(response, msg=msg)
		self.assertTrue(response['Content-Type'].startswith('application/json'), msg=msg)
		self.assertValidJSON(force_str(response.content), msg=msg)
	
	def assertResponseHasKeys(self, response, expected_keys, msg = None):
		'''Ensures that the data in a response has the expected keys'''
		self.assertGreaterEqual(self.deserialize(response).keys(), set(expected_keys), msg=msg)
	
	def assertGetDetailResponseContains(self, response, msg = None, **expected_values):
		'''Ensures that the data in a response from a GET on a detail URL has the expected values'''
		self.assertGreaterEqual(self.deserialize(response).items(), expected_values.items(), msg=msg)
	
	def assertGetListResponseContains(self, response, collection_name = 'objects', msg = None, **expected_values):
		'''Ensures that all the items in a response from a GET on a list URL has the expected values'''
		items = self.deserialize(response)[collection_name]
		for key, values in expected_values.items():
			with self.subTest(key = key):
				self.assertCountEqual((item[key] for item in items), values, msg=msg)
	
	def assertAttributesEqual(self, instance, expected_attributes, msg = None):
		'''Ensures that the object has the expected attributes with the expected values'''
		for attribute, value in expected_attributes.items():
			with self.subTest(attribute = attribute):
				self.assertEqual(getattr(instance, attribute), value, msg=msg)
	
	def assertObjectCreated(self, queryset, msg = None, **lookups):
		'''Ensures that the object has been created in the database'''
		self.assertEqual(queryset.filter(**lookups).count(), 1, msg=msg)
	
	def assertObjectDeleted(self, instance, msg = None):
		'''Ensures that the object has been deleted from the database'''
		with self.assertRaises(ObjectDoesNotExist, msg=msg):
			instance.refresh_from_db()


class ResourceTestCaseMixin(SvoApiTestCaseMixin):
	'''Test that the HTTP methods PUT/PATCH/DELETE are not allowed on the resource list URL, and that the HTTP methods POST/PUT are not allowed on the resource detail URL'''
	
	def setUp(self):
		super().setUp()
		# Define test data
		self.test_post_data = {}
		self.test_patch_data = {}
		self.test_instance = None
	
	def get_test_instance(self):
		'''Returns an an existing instance for use to test the detail URL'''
		if self.test_instance is None:
			raise NotImplementedError('You must override self.test_instance in the setUp method or override the get_test_instance method')
		return self.test_instance
	
	def get_test_post_data(self, **kwargs):
		'''Returns a dict for use as the data parameter to POST'''
		return dict(self.test_post_data, **kwargs)
	
	def get_test_patch_data(self, **kwargs):
		'''Returns a dict for use as the data parameter to PATCH/PUT'''
		return dict(self.test_patch_data, **kwargs)
	
	def test_get_list(self):
		'''Test a GET on the list URL'''
		self.fail('No test defined for a GET on the list URL')
	
	def test_post_list(self):
		'''Test a POST on the list URL'''
		self.fail('No test defined for a POST on the list URL')
	
	def test_put_list(self):
		'''Test a PUT on the list URL'''
		
		msg = 'A PUT on the list URL must return a not allowed response'
		data = {
			'objects': [self.get_test_post_data()]
		}
		response = self.api_client.put(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpMethodNotAllowed(response, msg=msg)
	
	def test_patch_list(self):
		'''Test a PATCH on the list URL'''
		
		msg = 'A PATCH on the list URL must return a not allowed response'
		data = {
			'objects': [self.get_test_post_data()],
			'deleted_objects' : [self.get_resource_uri(self.get_test_instance())]
		}
		response = self.api_client.patch(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpMethodNotAllowed(response, msg=msg)
	
	def test_delete_list(self):
		'''Test a DELETE on the list URL'''
		
		msg = 'A DELETE on the list URL must return a not allowed response'
		response = self.api_client.patch(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertHttpMethodNotAllowed(response, msg=msg)
	
	def test_get_detail(self):
		'''Test a GET on the detail URL'''
		
		self.fail('No test defined for a GET on the detail URL')
	
	def test_post_detail(self):
		'''Test a POST on the detail URL'''
		
		msg = 'A POST on the detail URL must return a not allowed response'
		data = self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(self.get_test_instance()), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpMethodNotAllowed(response, msg=msg)
	
	def test_put_detail(self):
		'''Test a PUT on the detail URL'''
		
		msg = 'A PUT on the detail URL must return a not allowed response'
		data = self.get_test_patch_data()
		response = self.api_client.put(self.get_resource_uri(self.get_test_instance()), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpMethodNotAllowed(response, msg=msg)
	
	def test_patch_detail(self):
		'''Test a PATCH on the detail URL'''
		
		self.fail('No test defined for a PATCH on the detail URL')
	
	def test_delete_detail(self):
		'''Test a DELETE on the detail URL'''
		
		self.fail('No test defined for a DELETE on the detail URL')


class ReadOnlyResourceTestCaseMixin(ResourceTestCaseMixin):
	'''Test that the HTTP methods POST/PUT/PATCH/DELETE are not allowed on the resource list nor detail URL'''
	
	def test_post_list(self):
		'''Test a POST on the list URL'''
		
		msg = 'A POST on the list URL must return a not allowed response'
		data = self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpMethodNotAllowed(response, msg=msg)
	
	def test_patch_detail(self):
		'''Test a PATCH on the detail URL'''
		
		msg = 'A PATCH on the detail URL must return a not allowed response'
		data = self.get_test_patch_data()
		response = self.api_client.patch(self.get_resource_uri(self.get_test_instance()), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpMethodNotAllowed(response, msg=msg)
	
	def test_delete_detail(self):
		'''Test a DELETE on the detail URL'''
		
		msg = 'A DELETE on the detail URL must return a not allowed response'
		response = self.api_client.patch(self.get_resource_uri(self.get_test_instance()), format='json', authentication=self.test_user_authentication)
		self.assertHttpMethodNotAllowed(response, msg=msg)
