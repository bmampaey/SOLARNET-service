from urllib.parse import urlencode
from django.test import TestCase

from dataset.models import Characteristic
from dataset.tests.utils import create_test_dataset
from api.tests.mixins import ReadOnlyResourceTestCaseMixin

class TestDatasetResource(ReadOnlyResourceTestCaseMixin, TestCase):
	'''Test the DatasetResource'''
	
	resource_name = 'dataset'
	
	def setUp(self):
		super().setUp()
		
		# Create test data
		self.test_characteristic1 = Characteristic.objects.create(name = 'test characteristic1')
		self.test_characteristic2 = Characteristic.objects.create(name = 'test characteristic2')
		self.test_characteristic3 = Characteristic.objects.create(name = 'test characteristic3')
		self.test_dataset1 = create_test_dataset(name = 'test dataset 1', characteristic_names = [self.test_characteristic1.name])
		self.test_metadata = self.test_dataset1.metadata_model.objects.create(oid='test_metadata')
		self.test_dataset2 = create_test_dataset(name = 'test dataset 2', metadata_model = None, characteristic_names = [self.test_characteristic1.name, self.test_characteristic2.name])
		
		self.test_instance = self.test_dataset1
	
	def test_get_list(self):
		'''Test a GET on the list URL'''
		
		msg = 'When no authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of datasets'
		response = self.api_client.get(self.get_resource_uri(), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, name = [self.test_dataset1.name, self.test_dataset2.name], msg=msg)
		
		msg = 'When authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of datasets'
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, name = [self.test_dataset1.name, self.test_dataset2.name], msg=msg)
	
	def test_get_list_filtered_characteristic(self):
		'''Test the characteristic filter for a GET on the list URL'''
		
		msg = 'When a exact filter for an existing charcteristic is requested, the list of dataset with that characteristic must be returned'
		data = {'characteristics': self.test_characteristic2.name}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, name = [self.test_dataset2.name], msg=msg)
		
		msg = 'When a exact filter for an non-existing characteristic is requested, no dataset must be returned'
		data = {'characteristics': 'does not exist'}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, name = [], msg=msg)
		
		msg = 'When a exact filter for an existing characteristic and a simple filter is requested, the list of dataset with that characteristic that conform to the simple filter must be returned'
		data = {'characteristics': self.test_characteristic1.name, 'name': self.test_dataset1.name}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, name = [self.test_dataset1.name], msg=msg)
		
		# The following test demonstrates that we correctly handle the __in filter, as we use distinct
		msg = 'When a __in filter is requested, the list of dataset with these characteristics must be returned'
		data = {'characteristics__in': ','.join([self.test_characteristic1.name, self.test_characteristic2.name])}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, name = [self.test_dataset1.name, self.test_dataset2.name], msg=msg)
	
	def test_get_list_metadata(self):
		'''Test the metadata field for a GET on the list URL'''
		
		metadata_resource_list_url = self.get_resource_uri(resource_name='base_metadata_test_resource')
		
		msg = 'When no filter is requested, the metadata field resource_uri must be exactly the metadata ressource list url'
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, metadata = [{'resource_uri': metadata_resource_list_url, 'estimated_count': 1}, None], msg=msg)
		
		msg = 'When a simple filter for the dataset resource is requested, the metadata field resource_uri must be exactly the metadata ressource list url'
		data = {'characteristics': self.test_characteristic1.name}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, metadata = [{'resource_uri': metadata_resource_list_url, 'estimated_count': 1}, None], msg=msg)
		
		msg = 'When a simple filter for the metadata resource is requested, the metadata field resource_uri must include the filter'
		data = {'oid': self.test_metadata.oid}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json',authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, metadata = [{'resource_uri': metadata_resource_list_url + '?' + urlencode(data), 'estimated_count': 1}, None], msg=msg)
		
		msg = 'When multiple filters for the metadata resource are requested, the metadata field resource_uri must include the filters'
		data = {'oid': self.test_metadata.oid, 'date_beg__isnull': True}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, metadata = [{'resource_uri': metadata_resource_list_url + '?' + urlencode(data), 'estimated_count': 1}, None], msg=msg)
		
		msg = 'When mixed filters for the dataset resource and the metadata resource are requested, the metadata field resource_uri must include the filters only for teh metadata resource'
		data = {'oid': self.test_metadata.oid, 'characteristics': self.test_characteristic1.name}
		response = self.api_client.get(self.get_resource_uri(), data=data, format='json', authentication=self.test_user_authentication)
		self.assertGetListResponseContains(response, metadata = [{'resource_uri': metadata_resource_list_url + '?' + urlencode({'oid': self.test_metadata.oid}), 'estimated_count': 1}, None], msg=msg)
	
	def test_get_detail(self):
		'''Test a GET on the detail URL'''
		
		msg = 'When no authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_dataset1), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['name', 'description', 'archive_url', 'telescope', 'instrument', 'characteristics', 'metadata'], msg=msg)
		
		msg = 'When authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_dataset1), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['name', 'description', 'archive_url', 'telescope', 'instrument', 'characteristics', 'metadata'], msg=msg)
	
	def test_get_detail_metadata(self):
		'''Test the metadata field for a GET on the detail URL'''
		
		metadata_resource_list_url = self.get_resource_uri(resource_name='base_metadata_test_resource')
		
		msg = 'When the dataset metadata_content_type is correctly set, the metadata field must be a dict with the metadata ressource list url and the estimated count'
		response = self.api_client.get(self.get_resource_uri(self.test_dataset1), format='json', authentication=self.test_user_authentication)
		self.assertGetDetailResponseContains(response, metadata = {'resource_uri': metadata_resource_list_url, 'estimated_count': 1}, msg=msg)
		
		msg = 'When the dataset metadata_content_type is None, the metadata field must be None'
		response = self.api_client.get(self.get_resource_uri(self.test_dataset2), format='json', authentication=self.test_user_authentication)
		self.assertGetDetailResponseContains(response, metadata = None, msg=msg)
