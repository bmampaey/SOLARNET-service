from django.test import TestCase

from dataset.tests.mixins import TestAdminMixin
from dataset.models import Keyword, KeywordType

class TestKeywordAdmin(TestAdminMixin, TestCase):
	'''Test the KeywordAdmin'''
	
	def setUp(self):
		super().setUp()
		# Create a keyword for the test dataset
		self.test_dataset_keyword = self.test_dataset.keywords.create(
			name = 'test',
			verbose_name = 'Test',
			type = KeywordType.TEXT,
			description = 'A test keyword'
		)
		
		# Create a keyword for the other dataset
		self.other_dataset_keyword = self.other_dataset.keywords.create(
			name = 'other_test',
			verbose_name = 'Other Test',
			type = KeywordType.TEXT,
			description = 'An other test keyword'
		)
	
	def test_index(self):
		'''Test a GET on the index URL'''
		
		msg = 'The other user must see the keyword list URL in the index view'
		self.client.force_login(self.other_user)
		response = self.client.get(self.index_url)
		self.assertInHtmlResponse(response, self.get_list_url(Keyword), msg=msg)
		
		msg = 'The test user must see the keyword list URL in the index view'
		self.client.force_login(self.test_user)
		response = self.client.get(self.index_url)
		self.assertInHtmlResponse(response, self.get_list_url(Keyword), msg=msg)
		
		msg = 'The super user must see the keyword list URL in the index view'
		self.client.force_login(self.super_user)
		response = self.client.get(self.index_url)
		self.assertInHtmlResponse(response, self.get_list_url(Keyword), msg=msg)
	
	def test_list_url(self):
		'''Test a GET on the list URL'''
		
		msg = 'The other user must NOT see the keyword of the test dataset in the list view'
		self.client.force_login(self.other_user)
		response = self.client.get(self.get_list_url(Keyword))
		self.assertNotInHtmlResponse(response, self.get_change_url(self.test_dataset_keyword), msg=msg)
		
		msg = 'The test user must see the keyword of the test dataset in the list view, but not of the other dataset'
		self.client.force_login(self.test_user)
		response = self.client.get(self.get_list_url(Keyword))
		self.assertInHtmlResponse(response, self.get_change_url(self.test_dataset_keyword), msg=msg)
		self.assertNotInHtmlResponse(response, self.get_change_url(self.other_dataset_keyword), msg=msg)
		
		msg = 'The super user must see all the keywords in the list view'
		self.client.force_login(self.super_user)
		response = self.client.get(self.get_list_url(Keyword))
		self.assertInHtmlResponse(response, self.get_change_url(self.test_dataset_keyword), self.get_change_url(self.other_dataset_keyword), msg=msg)
	
	def test_add_url(self):
		'''Test a POST on the add URL'''
		
		test_post_data = {
			'dataset': self.test_dataset.pk,
			'name': 'new_name',
			'verbose_name': 'New Name',
			'type': KeywordType.TEXT,
			'unit': 'new unit',
			'description': 'new description'
		}
		
		msg = 'The other user may NOT add a new keyword to the test dataset'
		self.client.force_login(self.other_user)
		response = self.client.post(self.get_add_url(Keyword), data = test_post_data)
		self.assertHttpForbidden(response, msg=msg)
		
		msg = 'The test user may NOT add a new keyword to the test dataset'
		self.client.force_login(self.test_user)
		response = self.client.post(self.get_add_url(Keyword), data = test_post_data)
		self.assertHttpForbidden(response, msg=msg)
		
		msg = 'The super user may add a new keyword to any dataset'
		self.client.force_login(self.super_user)
		response = self.client.post(self.get_add_url(Keyword), data = test_post_data)
		self.assertRedirects(response, self.get_list_url(Keyword), msg_prefix=msg)
	
	def test_delete_url(self):
		'''Test a POST on the delete URL'''
		
		test_post_data = {
			'post':'yes'
		}
		
		msg = 'The other user may NOT delete a keyword of the test dataset'
		self.client.force_login(self.other_user)
		response = self.client.post(self.get_delete_url(self.test_dataset_keyword), data = test_post_data)
		self.assertHttpForbidden(response, msg=msg)
		
		msg = 'The test user may NOT delete a keyword of the test dataset'
		self.client.force_login(self.test_user)
		response = self.client.post(self.get_delete_url(self.test_dataset_keyword), data = test_post_data)
		self.assertHttpForbidden(response, msg=msg)
		
		msg = 'The super user may delete any keyword'
		self.client.force_login(self.super_user)
		response = self.client.post(self.get_delete_url(self.test_dataset_keyword), data = test_post_data)
		self.assertRedirects(response, self.get_list_url(Keyword), msg_prefix=msg)
	
	def test_change_url(self):
		'''Test a POST on the change URL'''
		
		test_post_data1 = {
			'dataset': self.other_dataset.pk,
			'name': 'other_name1',
			'verbose_name': 'Other Name 1',
			'type': KeywordType.INTEGER,
			'unit': 'other unit 1',
			'description': 'other description 1'
		}
		
		test_post_data2 = {
			'dataset': self.other_dataset.pk,
			'name': 'other_name2',
			'verbose_name': 'Other Name 2',
			'type': KeywordType.REAL,
			'unit': 'other unit 2',
			'description': 'other description 2'
		}
		
		msg = 'The other user may NOT change the dataset, name, verbose_name, type, unit, and description of a keyword of the test dataset'
		self.client.force_login(self.other_user)
		response = self.client.post(self.get_change_url(self.test_dataset_keyword), data = test_post_data1)
		self.assertHttpForbidden(response, msg=msg)
		self.assertObjectUpdated(self.test_dataset_keyword, msg=msg)
		
		msg = 'The test user may change the verbose_name, unit, and description BUT not the dataset, name, and type of a keyword of the test dataset'
		self.client.force_login(self.test_user)
		response = self.client.post(self.get_change_url(self.test_dataset_keyword), data = test_post_data1)
		self.assertRedirects(response, self.get_list_url(Keyword), msg_prefix=msg)
		self.assertObjectUpdated(self.test_dataset_keyword, 'verbose_name', 'unit', 'description', msg=msg)
		
		msg = 'The super user may change the dataset, name, verbose_name, type, unit, and description of any keyword'
		self.client.force_login(self.super_user)
		response = self.client.post(self.get_change_url(self.test_dataset_keyword), data = test_post_data2)
		self.assertRedirects(response, self.get_list_url(Keyword), msg_prefix=msg)
		self.assertObjectUpdated(self.test_dataset_keyword, 'dataset', 'name', 'verbose_name', 'type', 'unit', 'description', msg=msg)
