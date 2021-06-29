from django.test import TestCase

from dataset.tests.utils import create_test_dataset
from api.tests.mixins import ReadOnlyResourceTestCaseMixin


class TestInstrumentResource(ReadOnlyResourceTestCaseMixin, TestCase):
	'''Test the InstrumentResource'''
	
	resource_name = 'instrument'
	
	def setUp(self):
		super().setUp()
		# Create test data
		self.test_dataset = create_test_dataset()
		self.test_instrument = self.test_dataset.instrument
		self.test_instance = self.test_instrument
	
	def test_get_list(self):
		'''Test a GET on the list URL'''
		
		msg = 'When no authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of instruments'
		response = self.api_client.get(self.get_resource_uri(), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, name = [self.test_instrument.name], msg=msg)
		
		msg = 'When authentication is provided, a GET on the list URL must return a valid JSON response with the complete list of instruments'
		response = self.api_client.get(self.get_resource_uri(), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertGetListResponseContains(response, name =  [self.test_instrument.name], msg=msg)
	
	def test_get_detail(self):
		'''Test a GET on the detail URL'''
		
		msg = 'When no authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_instrument), format='json')
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['name', 'description', 'telescope'], msg=msg)
		
		msg = 'When authentication is provided, a GET on the detail URL must return a valid JSON response'
		response = self.api_client.get(self.get_resource_uri(self.test_instrument), format='json', authentication=self.test_user_authentication)
		self.assertValidJSONResponse(response, msg=msg)
		self.assertResponseHasKeys(response, ['name', 'description', 'telescope'], msg=msg)
