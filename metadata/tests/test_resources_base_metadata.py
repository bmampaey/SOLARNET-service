from datetime import datetime, timezone
from django.test import TestCase
from django.contrib.auth.models import Permission

from api.constants import FILTERS
from api.tests.mixins import ResourceTestCaseMixin
from metadata.models import Tag
from dataset.tests.utils import create_test_dataset

class TestBaseMetadataResource(ResourceTestCaseMixin, TestCase):
	'''Test the BaseMetadataResource'''
	
	resource_name = 'base_metadata_test_resource'
	
	def setUp(self):
		super().setUp()
		# Create test data
		self.test_dataset = create_test_dataset()
		# Add the test user to the dataset user_group so that he has permission to do POST/PATCH/DELETE
		self.test_user.groups.add(self.test_dataset.user_group)
		self.test_tag1 = Tag.objects.create(name = 'test tag1')
		self.test_tag2 = Tag.objects.create(name = 'test tag2')
		self.test_tag3 = Tag.objects.create(name = 'test tag3')
		self.test_data_location1 = self.test_dataset.data_locations.create(file_url = 'https://test.com/file1.fits', file_size = 1, file_path = 'test_path/file1.fits', offline = False)
		self.test_data_location2 = self.test_dataset.data_locations.create(file_url = 'https://test.com/file2.fits', file_size = 2, file_path = 'test_path/file2.fits', offline = True)
		self.test_metadata1 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata1', data_location = self.test_data_location1)
		self.test_metadata2 = self.test_dataset.metadata_model.objects.create(oid = 'test_metadata2')
		self.test_metadata1.tags.add(self.test_tag1)
		self.test_metadata2.tags.add(self.test_tag1, self.test_tag2)
		
		self.test_instance = self.test_metadata1
		self.test_post_data = {
			'oid': 'test_metadata3',
			'fits_header': 'fits header',
			'date_beg' : datetime(2000, 1, 1, tzinfo = timezone.utc),
			'date_end': datetime(2000, 1, 1, 0, 0, 1, tzinfo = timezone.utc),
			'wavemin': 0,
			'wavemax': 1,
			'data_location': self.test_data_location1
		}
		self.test_patch_data = {
			'fits_header': 'new fits header',
			'date_beg' : datetime(2000, 1, 1, tzinfo = timezone.utc),
			'date_end': datetime(2000, 1, 1, 0, 0, 1, tzinfo = timezone.utc),
			'wavemin': 0,
			'wavemax': 1,
			'data_location': self.test_data_location2
		}
	
	def test_init(self):
		'''Test the __init__ method of the resource'''
		
		msg = 'When the resource is instanciated, the ordering must contain all regular field names'
		self.assertCountEqual(self.resource._meta.ordering, ['oid', 'fits_header', 'date_beg', 'date_end', 'wavemin', 'wavemax'], msg=msg)
		
		msg = 'When the resource is instanciated, the filtering must contain all field names and appropriate filters'
		self.assertDictEqual(self.resource._meta.filtering, {
			'tags': FILTERS.RELATIONAL,
			'search': FILTERS.COMPLEX_SEARCH_EXPRESSION,
			'oid' : FILTERS.TEXT,
			'fits_header': FILTERS.TEXT,
			'date_beg': FILTERS.DATETIME,
			'date_end': FILTERS.DATETIME,
			'wavemin': FILTERS.NUMERIC,
			'wavemax': FILTERS.NUMERIC
		}, msg=msg)
	
	def test_get_list(self):
		'''Test a GET on the list URL'''
		
		msg = 'When no authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of metadata'
		response = self.api_client.get(self.get_resource_uri(), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid, self.test_metadata2.oid], msg=msg)
		
		msg = 'When authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of metadata'
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid, self.test_metadata2.oid], msg=msg)
	
	def test_get_list_filtered(self):
		'''Test the filter for a GET on the list URL'''
		
		msg = 'When a simple filter for an existing keyword is requested, the list of metadata that conform to the simple filter must be returned'
		data = {'oid': self.test_metadata1.oid}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid], msg=msg)
		
		msg = 'When a simple filter for an non-existing keyword is requested, the entire list of metadata must be returned'
		data = {'characteristic__in': 'irrelevant'}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid, self.test_metadata2.oid], msg=msg)
		
		msg = 'When a mix of simple filters for existing and non-existing keywords are requested, the list of metadata that conform to the existing keyword filter must be returned'
		data = {'oid': self.test_metadata1.oid, 'characteristic__in': 'irrelevant'}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid], msg=msg)
	
	def test_get_list_filtered_tag(self):
		'''Test the tag filter for a GET on the list URL'''
		
		msg = 'When a exact filter for an existing tag is requested, the list of metadata with that tag must be returned'
		data = {'tags': self.test_tag2.name}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [self.test_metadata2.oid], msg=msg)
		
		msg = 'When a exact filter for an non-existing tag is requested, no metadata must be returned'
		data = {'tags': 'does not exist'}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [], msg=msg)
		
		msg = 'When a exact filter for an existing tag and a simple filter is requested, the list of metadata with that tag that conform to the simple filter must be returned'
		data = {'tags': self.test_tag1.name, 'oid': self.test_metadata1.oid}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid], msg=msg)
		
		# BUG: The following test demonstrates that we don't correctly handle the __in filter, as we should be using distinct
		msg = 'When a __in filter is requested, the list of metadata with these tags must be returned'
		data = {'tags__in': ','.join([self.test_tag1.name, self.test_tag2.name])}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid, self.test_metadata2.oid], msg=msg)
	
	def test_get_list_filtered_search(self):
		'''Test the search filter for a GET on the list URL'''
		
		msg = 'When a simple search lookup is requested, the usual list must be returned'
		data = {'search': 'oid=test_metadata1'}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid], msg=msg)
		
		msg = 'When a complex search expression is requested, the list respecting that expression must be returned'
		data = {'search': 'oid=test_metadata1 or oid=test_metadata2'}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid, self.test_metadata2.oid], msg=msg)
		
		msg = 'When two complex search expressions are requested, the list respecting both expressions must be returned'
		data = {'search': ['oid=test_metadata1 or oid=test_metadata2', 'not oid=test_metadata2']}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid], msg=msg)
		
		msg = 'When a complex search expression is requested and a simple filter is requested, the list respecting both must be returned'
		data = {'search': 'oid=test_metadata1 or oid=test_metadata2', 'oid': 'test_metadata1'}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, oid = [self.test_metadata1.oid], msg=msg)
		
		msg = 'When a complex search expression is requested for a non-existing keyword, a bad request response must be returned'
		data = {'search': 'characteristic__in=irrelevant'}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpBadRequest(response, msg=msg)
		
	
	def test_post_list(self):
		'''Test a POST on the list URL'''
		
		msg = 'When no authentication is provided, a POST on the list URL must return an unauthorized response'
		data = self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided but user has not permission, a POST on the list URL must return an unauthorized response'
		data = self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and user has permission, a POST on the list URL must return a created response and the metadata must exist in the database'
		self.test_user.user_permissions.add(Permission.objects.get(codename='add_basemetadatatest'))
		data = self.get_test_post_data()
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpCreated(response, msg=msg)
		self.assertObjectCreated(self.test_dataset.metadata_model.objects.all(), oid=data['oid'], msg=msg)
		
		msg = 'When authentication is provided and user has permission, a POST on the list URL with data_location must return a created response and the metadata and data location must exist in the database'
		self.test_user.user_permissions.add(Permission.objects.get(codename='add_datalocation'))
		data_location = {
			'dataset': self.test_dataset,
			'file_url': 'https://test.com/new_file.fits',
			'file_size': 2048,
			'file_path': 'test_path/new_file.fits',
			'offline': True
		}
		data = self.get_test_post_data(oid='test_metadata4', data_location=data_location)
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpCreated(response, msg=msg)
		self.assertObjectCreated(self.test_dataset.metadata_model.objects.all(), oid=data['oid'], data_location=self.test_dataset.data_locations.get(file_url = data_location['file_url']), msg=msg)
		
		msg = 'When authentication is provided and user has permission, a POST on the list URL with tags must return a created response and the metadata and tags must exist in the database'
		self.test_user.user_permissions.add(Permission.objects.get(codename='change_tag'))
		tags = [
			self.test_tag3,
			{'name': 'new tag'},
		]
		data = self.get_test_post_data(oid='test_metadata5', tags=tags)
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpCreated(response, msg=msg)
		self.assertObjectCreated(self.test_dataset.metadata_model.objects.all(), oid=data['oid'], msg=msg)
		self.assertQuerysetEqual(self.test_dataset.metadata_model.objects.filter(oid=data['oid']).values_list('tags__name', flat=True), [self.test_tag3.name, 'new tag'], ordered=False, msg=msg)
	
	def test_get_detail(self):
		'''Test a GET on the detail URL'''
		
		msg = 'When no authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_metadata1), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['oid', 'fits_header', 'data_location', 'tags', 'date_beg', 'date_end', 'wavemin', 'wavemax'], msg=msg)
		
		msg = 'When authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_metadata1), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['oid', 'fits_header', 'data_location', 'tags', 'date_beg', 'date_end', 'wavemin', 'wavemax'], msg=msg)
		
	def test_patch_detail(self):
		'''Test a PATCH on the detail URL'''
		
		msg = 'When no authentication is provided, a PATCH must return an unauthorized response'
		data = self.get_test_patch_data()
		response = self.api_client.patch(self.get_resource_uri(self.test_metadata1), data=data, format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided but user has not permission, a PATCH must return an unauthorized response'
		data = self.get_test_patch_data()
		response = self.api_client.patch(self.get_resource_uri(self.test_metadata1), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and user has permission, a PATCH must return an OK response and the metadata must have been updated'
		# WARNING if the metadata that is being modified has tags, it is necessary to have the change_tag permission even if the tags are not modified
		self.test_user.user_permissions.add(Permission.objects.get(codename='change_basemetadatatest'), Permission.objects.get(codename='change_tag'))
		data = self.get_test_patch_data()
		response = self.api_client.patch(self.get_resource_uri(self.test_metadata1), data=data, format='json', authentication=self.test_user_authentication)
		self.test_metadata1.refresh_from_db()
		self.assertHttpAccepted(response, msg=msg)
		self.assertAttributesEqual(self.test_metadata1, data, msg=msg)
	
	def test_delete_detail(self):
		'''Test a DELETE on the detail URL'''
		
		msg = 'When no authentication is provided, a DELETE must return an unauthorized response'
		response = self.api_client.delete(self.get_resource_uri(self.test_metadata1), format='json')
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided but user has not permission, a DELETE must return an unauthorized response'
		response = self.api_client.delete(self.get_resource_uri(self.test_metadata1), format='json', authentication=self.test_user_authentication)
		self.assertHttpUnauthorized(response, msg=msg)
		
		msg = 'When authentication is provided and user has permission, a DELETE must return an empty response and the metadata must have been deleted'
		self.test_user.user_permissions.add(Permission.objects.get(codename='delete_basemetadatatest'))
		response = self.api_client.delete(self.get_resource_uri(self.test_metadata1), format='json', authentication=self.test_user_authentication)
		self.assertHttpAccepted(response, msg=msg)
		self.assertObjectDeleted(self.test_metadata1, msg=msg)
	
	def test_validation_errors(self):
		'''Test that creating/updating metadata with invalid data return appropriate error messages'''
		
		# Give user permission to create/update
		self.test_user.user_permissions.add(Permission.objects.get(codename='add_basemetadatatest'), Permission.objects.get(codename='change_basemetadatatest'), Permission.objects.get(codename='change_tag'))
		
		msg = 'When a metadata with the same oid already exists, a POST must return a bad request with a proper error message'
		data = self.get_test_post_data(oid = self.test_metadata1.oid)
		response = self.api_client.post(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpBadRequest(response, msg=msg)
		self.assertIn('oid', response.content.decode(response.charset), msg=msg)
		
		msg = 'When oid is specified, a PATCH must return a bad request with a proper error message'
		data = self.get_test_patch_data(oid = 'test_metadata1_updated')
		response = self.api_client.patch(self.get_resource_uri(self.test_metadata1), data=data, format='json', authentication=self.test_user_authentication)
		self.assertHttpBadRequest(response, msg=msg)
		self.assertIn('oid', response.content.decode(response.charset), msg=msg)
