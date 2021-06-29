from django.test import TestCase
from django.contrib.auth.models import Permission

from metadata.models import Tag
from api.tests.mixins import ReadOnlyResourceTestCaseMixin
from dataset.tests.utils import create_test_dataset

# The TagResource is mainly readonly, the POST method is allowed, but not the PUT/PATCH/DELETE methods
class TestTagResource(ReadOnlyResourceTestCaseMixin, TestCase):
	'''Test the TagResource'''
	
	resource_name = 'tag'
	
	def setUp(self):
		super().setUp()
		# Create test data
		self.test_dataset = create_test_dataset()
		self.test_tag1 = Tag.objects.create(name = 'test tag1')
		self.test_tag2 = Tag.objects.create(name = 'test tag2')
		self.test_tag3 = Tag.objects.create(name = 'test tag3')
		self.test_metadata1 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata1')
		self.test_metadata2 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata2')
		self.test_metadata1.tags.add(self.test_tag1)
		self.test_metadata2.tags.add(self.test_tag1, self.test_tag2)
		self.test_instance = self.test_tag1
		self.test_post_data = {'name': 'new tag'}
		self.test_patch_data = {'name': 'other name'}
	
	def test_get_list(self):
		'''Test a GET on the list URL'''
		
		msg = 'When no authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of tags'
		response = self.api_client.get(self.get_resource_uri(), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, name = [self.test_tag1.name, self.test_tag2.name, self.test_tag3.name], msg=msg)
		
		msg = 'When authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of tags'
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, name = [self.test_tag1.name, self.test_tag2.name, self.test_tag3.name], msg=msg)
	
	def test_get_list_filtered(self):
		'''Test the dataset filter for a GET on the list URL'''
		
		msg = 'When a simple filter is requested, the usual list must be returned'
		data = {'name': self.test_tag1.name}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, name = [self.test_tag1.name], msg=msg)
		
		msg = 'When a dataset filter for an existing dataset is requested, only the tags related to the dataset metadata must be returned'
		data = {'dataset': 'test dataset'}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, name = [self.test_tag1.name, self.test_tag2.name], msg=msg)
		
		msg = 'When a dataset filter for an existing dataset and a simple filter is requested, only the tags related to the dataset metadata that conform to the simple filter must be returned'
		data = {'dataset': 'test dataset', 'name': self.test_tag1.name}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, name = [self.test_tag1.name], msg=msg)
		
		msg = 'When a dataset filter for an non-existing dataset is requested, no tags must be returned'
		data = {'dataset': 'does not exist'}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, name = [], msg=msg)
	
	def test_post_list(self):
		'''Test a POST on the list URL'''
		
		msg = 'When no authentication is provided, a POST on the list URL must return an unauthorized response'
		data=self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided but user has not permission, a POST on the list URL must return an unauthorized response'
		data=self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and user has permission, a POST on the list URL must return a created response and the tag must exists in the database'
		data = self.get_test_post_data()
		# Note there is a bug in tastypie and it checks the change permission instead of the add permission
		self.test_user.user_permissions.add(Permission.objects.get(codename='change_tag'))
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpCreated(response, msg=msg)
		self.assertObjectCreated(Tag.objects.all(), name = data['name'], msg=msg)
		
	def test_get_detail(self):
		'''Test a GET on the detail URL'''
		
		msg = 'When no authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_tag1), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['name'], msg=msg)
		
		msg = 'When authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_tag1), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['name'], msg=msg)
	
	def test_validation_errors(self):
		'''Test that creating/updating tag with invalid data return appropriate error messages'''
		
		# Give user permission to create/update
		self.test_user.user_permissions.add(Permission.objects.get(codename='change_tag'))
		
		msg = 'When a tag with the same name already exists, a POST must return a bad request with a proper error message'
		data = self.get_test_post_data(name = self.test_tag1.name)
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpBadRequest(response, msg=msg)
		self.assertIn('name', response.content.decode(response.charset), msg=msg)
