from django.test import TestCase

from dataset.tests.mixins import TestAdminMixin
from dataset.models import Dataset
from .utils import create_test_instrument


class TestDatasetAdmin(TestAdminMixin, TestCase):
	'''Test the DatasetAdmin'''
	
	def test_index(self):
		'''Test a GET on the index URL'''
		
		msg = 'The other user must see the dataset list URL in the index view'
		self.client.force_login(self.other_user)
		response = self.client.get(self.index_url)
		self.assertInHtmlResponse(response, self.get_list_url(Dataset), msg=msg)
		
		msg = 'The test user must see the dataset list URL in the index view'
		self.client.force_login(self.test_user)
		response = self.client.get(self.index_url)
		self.assertInHtmlResponse(response, self.get_list_url(Dataset), msg=msg)
		
		msg = 'The super user must see the dataset list URL in the index view'
		self.client.force_login(self.super_user)
		response = self.client.get(self.index_url)
		self.assertInHtmlResponse(response, self.get_list_url(Dataset), msg=msg)
	
	def test_list_url(self):
		'''Test a GET on the list URL'''
		
		msg = 'The other user must NOT see the test dataset in the list view'
		self.client.force_login(self.other_user)
		response = self.client.get(self.get_list_url(Dataset))
		self.assertNotInHtmlResponse(response, self.get_change_url(self.test_dataset), msg=msg)
		
		msg = 'The test user must see the test dataset in the list view'
		self.client.force_login(self.test_user)
		response = self.client.get(self.get_list_url(Dataset))
		self.assertInHtmlResponse(response, self.get_change_url(self.test_dataset), msg=msg)
		
		msg = 'The super user must see the test dataset in the list view'
		self.client.force_login(self.super_user)
		response = self.client.get(self.get_list_url(Dataset))
		self.assertInHtmlResponse(response, self.get_change_url(self.test_dataset), msg=msg)
	
	def test_add_url(self):
		'''Test a POST on the add URL'''
		
		test_post_data = {
			'name': 'new test dataset',
			'telescope': self.test_dataset.telescope.pk,
			'instrument': self.test_dataset.instrument.pk
		}
		
		msg = 'The other user may NOT add a new dataset'
		self.client.force_login(self.other_user)
		response = self.client.post(self.get_add_url(Dataset), data = test_post_data)
		self.assertHttpForbidden(response, msg=msg)
		
		msg = 'The test user may NOT add a new dataset'
		self.client.force_login(self.test_user)
		response = self.client.post(self.get_add_url(Dataset), data = test_post_data)
		self.assertHttpForbidden(response, msg=msg)
		
		msg = 'The super user may add a new dataset'
		self.client.force_login(self.super_user)
		response = self.client.post(self.get_add_url(Dataset), data = test_post_data)
		self.assertRedirects(response, self.get_list_url(Dataset), msg_prefix=msg)
	
	def test_delete_url(self):
		'''Test a POST on the delete URL'''
		
		test_post_data = {
			'post':'yes'
		}
		
		msg = 'The other user may NOT delete the test dataset'
		self.client.force_login(self.other_user)
		response = self.client.post(self.get_delete_url(self.test_dataset), data = test_post_data)
		self.assertHttpForbidden(response, msg=msg)
		
		msg = 'The test user may NOT delete the test dataset'
		self.client.force_login(self.test_user)
		response = self.client.post(self.get_delete_url(self.test_dataset), data = test_post_data)
		self.assertHttpForbidden(response, msg=msg)
		
		msg = 'The super user may delete the test dataset'
		self.client.force_login(self.super_user)
		response = self.client.post(self.get_delete_url(self.test_dataset), data = test_post_data)
		self.assertRedirects(response, self.get_list_url(Dataset), msg_prefix=msg)
	
	def test_change_url(self):
		'''Test a POST on the change URL'''
		
		other_instrument = create_test_instrument('other instrument', 'other telescope')
		
		test_post_data = {
			'name': 'other name',
			'description': 'other description',
			'contact_email': 'other_email@test.com',
			'archive_url': 'http://other-url.test.com',
			'telescope': other_instrument.telescope.name,
			'instrument': other_instrument.name,
			'characteristics': [],
			'user_group': '',
			'metadata_content_type': ''
		}
		
		msg = 'The other user may NOT change the description, contact_email, archive_url and characteristics, NEITHER the name, telescope, instrument, user_group and metadata_content_type of the test dataset'
		self.client.force_login(self.other_user)
		response = self.client.post(self.get_change_url(self.test_dataset), data = test_post_data)
		self.assertHttpForbidden(response, msg=msg)
		self.assertObjectUpdated(self.test_dataset, msg=msg)
		
		msg = 'The test user may change the description, contact_email, archive_url and characteristics, but NOT the name, telescope, instrument, user_group and metadata_content_type of the test dataset'
		self.client.force_login(self.test_user)
		response = self.client.post(self.get_change_url(self.test_dataset), data = test_post_data)
		self.assertRedirects(response, self.get_list_url(Dataset), msg_prefix=msg)
		self.assertObjectUpdated(self.test_dataset, 'description', 'contact_email', 'archive_url', msg=msg)
		# characteristics is a many to many, and cannot be tested by assertObjectUpdated
		self.assertQuerysetEqual(self.test_dataset.characteristics.all(), [], msg=msg)
		
		msg = 'The super user may change description, contact_email, archive_url and characteristics, and also the name, telescope, instrument, user_group and metadata_content_type of any dataset'
		self.client.force_login(self.super_user)
		response = self.client.post(self.get_change_url(self.test_dataset), data = test_post_data)
		self.assertRedirects(response, self.get_list_url(Dataset), msg_prefix=msg)
		# description, contact_email, archive_url and characteristics have already been updated during previous test
		self.assertObjectUpdated(self.test_dataset, 'name', 'telescope', 'instrument', 'user_group', 'metadata_content_type', msg=msg)
