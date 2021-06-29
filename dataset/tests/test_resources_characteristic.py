from django.test import TestCase

from dataset.tests.utils import create_test_dataset
from api.tests.mixins import ReadOnlyResourceTestCaseMixin


class TestCharacteristicResource(ReadOnlyResourceTestCaseMixin, TestCase):
	'''Test the CharacteristicResource'''
	
	resource_name = 'characteristic'
	
	def setUp(self):
		super().setUp()
		# Create test data
		self.test_dataset = create_test_dataset(characteristic_names = ['test characteristic'])
		self.test_characteristic = self.test_dataset.characteristics.get(name='test characteristic')
		self.test_instance = self.test_characteristic
	
	def test_get_list(self):
		'''Test a GET on the list URL'''
		
		msg = 'When no authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of characteristics'
		response = self.api_client.get(self.get_resource_uri(), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, name = [self.test_characteristic.name], msg=msg)
		
		msg = 'When authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of characteristics'
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, name = [self.test_characteristic.name], msg=msg)
	
	def test_get_detail(self):
		'''Test a GET on the detail URL'''
		
		msg = 'When no authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_characteristic), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['name', 'datasets'], msg=msg)
		
		msg = 'When authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_characteristic), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['name', 'datasets'], msg=msg)
