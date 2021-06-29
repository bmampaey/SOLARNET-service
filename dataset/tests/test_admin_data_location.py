from django.test import TestCase
from django.forms import ModelChoiceField

from dataset.tests.mixins import TestAdminMixin
from dataset.models import DataLocation


class TestDataLocationAdmin(TestAdminMixin, TestCase):
	'''Test the DataLocationAdmin'''
	
	def setUp(self):
		super().setUp()
		# Create a data location for the test dataset
		self.test_dataset_datalocation = self.test_dataset.data_locations.create(
			file_url = 'https://test.dataset.com/file.fits',
			file_size = 1024,
			file_path = 'test_path/file.fits',
			offline=False
		)
		
		# Create a data location for the other dataset
		self.other_dataset_datalocation = self.other_dataset.data_locations.create(
			file_url = 'https://other.dataset.com/file.fits',
			file_size = 1024,
			file_path = 'test_path/file.fits',
			offline=False
		)
	
	def test_index(self):
		'''Test a GET on the index URL'''
		
		msg = 'The other user must see the data location list URL in the index view'
		self.client.force_login(self.other_user)
		response = self.client.get(self.index_url)
		self.assertInHtmlResponse(response, self.get_list_url(DataLocation), msg=msg)
		
		msg = 'The test user must see the data location list URL in the index view'
		self.client.force_login(self.test_user)
		response = self.client.get(self.index_url)
		self.assertInHtmlResponse(response, self.get_list_url(DataLocation), msg=msg)
		
		msg = 'The super user must see the data location list URL in the index view'
		self.client.force_login(self.super_user)
		response = self.client.get(self.index_url)
		self.assertInHtmlResponse(response, self.get_list_url(DataLocation), msg=msg)
	
	def test_list_url(self):
		'''Test a GET on the list URL'''
		
		msg = 'The other user must NOT see the data location of the test dataset in the list view'
		self.client.force_login(self.other_user)
		response = self.client.get(self.get_list_url(DataLocation))
		self.assertNotInHtmlResponse(response, self.get_change_url(self.test_dataset_datalocation), msg=msg)
		
		msg = 'The test user must see the data location of the test dataset in the list view, but not of the other dataset'
		self.client.force_login(self.test_user)
		response = self.client.get(self.get_list_url(DataLocation))
		self.assertInHtmlResponse(response, self.get_change_url(self.test_dataset_datalocation), msg=msg)
		self.assertNotInHtmlResponse(response, self.get_change_url(self.other_dataset_datalocation), msg=msg)
		
		msg = 'The super user must see all the data locations in the list view'
		self.client.force_login(self.super_user)
		response = self.client.get(self.get_list_url(DataLocation))
		self.assertInHtmlResponse(response, self.get_change_url(self.test_dataset_datalocation), self.get_change_url(self.other_dataset_datalocation), msg=msg)
	
	def test_add_url(self):
		'''Test a POST on the add URL'''
		
		test_post_data1 = {
			'dataset': self.test_dataset.pk,
			'file_url': 'https://test.dataset.com/new_file1.fits',
			'file_size': 1024,
			'file_path': 'test_path/new_file1.fits',
			'thumbnail_url': 'https://test.dataset.com/new_file1.png',
			'offline': True
		}
		
		test_post_data2 = {
			'dataset': self.test_dataset.pk,
			'file_url': 'https://test.dataset.com/new_file2.fits',
			'file_size': 1024,
			'file_path': 'test_path/new_file2.fits',
			'thumbnail_url': 'https://test.dataset.com/new_file2.png',
			'offline': True
		}
		
		msg = 'The other user may NOT add a new data location to the test dataset'
		self.client.force_login(self.other_user)
		response = self.client.post(self.get_add_url(DataLocation), data = test_post_data1)
		self.assertHttpOK(response, msg=msg)
		self.assertFormError(response, 'adminform', 'dataset', ModelChoiceField.default_error_messages['invalid_choice'], msg_prefix=msg)
		
		msg = 'The test user may add a new data location to the test dataset'
		self.client.force_login(self.test_user)
		response = self.client.post(self.get_add_url(DataLocation), data = test_post_data1)
		self.assertRedirects(response, self.get_list_url(DataLocation), msg_prefix=msg)
		
		msg = 'The super user may add a new data location to any dataset'
		self.client.force_login(self.super_user)
		response = self.client.post(self.get_add_url(DataLocation), data = test_post_data2)
		self.assertRedirects(response, self.get_list_url(DataLocation), msg_prefix=msg)
	
	def test_delete_url(self):
		'''Test a POST on the delete URL'''
		
		test_post_data = {
			'post':'yes'
		}
		
		msg = 'The other user may NOT delete a data location of the test dataset'
		self.client.force_login(self.other_user)
		response = self.client.post(self.get_delete_url(self.test_dataset_datalocation), data = test_post_data)
		self.assertHttpForbidden(response, msg=msg)
		
		msg = 'The test user may delete a data location of the test dataset'
		self.client.force_login(self.test_user)
		response = self.client.post(self.get_delete_url(self.test_dataset_datalocation), data = test_post_data)
		self.assertRedirects(response, self.get_list_url(DataLocation), msg_prefix=msg)
		
		msg = 'The super user may delete any data location'
		self.client.force_login(self.super_user)
		response = self.client.post(self.get_delete_url(self.other_dataset_datalocation), data = test_post_data)
		self.assertRedirects(response, self.get_list_url(DataLocation), msg_prefix=msg)
	
	def test_change_url(self):
		'''Test a POST on the change URL'''
		
		test_post_data1 = {
			'dataset': self.test_dataset.pk,
			'file_url': 'https://test.dataset.com/new_file1.fits',
			'file_size': 1025,
			'file_path': 'test_path/new_file1.fits',
			'thumbnail_url': 'https://test.dataset.com/new_file1.png',
			'offline': True
		}
		
		test_post_data2 = {
			'dataset': self.other_dataset.pk,
			'file_url': 'https://test.dataset.com/new_file2.fits',
			'file_size': 1026,
			'file_path': 'test_path/new_file2.fits',
			'thumbnail_url': 'https://test.dataset.com/new_file2.png',
		}
		
		msg = 'The other user may NOT change the file_url, file_size, file_path, thumbnail_url, and offline of a data location of the test dataset'
		self.client.force_login(self.other_user)
		response = self.client.post(self.get_change_url(self.test_dataset_datalocation), data = test_post_data1)
		self.assertHttpForbidden(response, msg=msg)
		self.assertObjectUpdated(self.test_dataset_datalocation, msg=msg)
		
		msg = 'The test user may change the file_url, file_size, file_path, thumbnail_url, and offline of a data location of the test dataset'
		self.client.force_login(self.test_user)
		response = self.client.post(self.get_change_url(self.test_dataset_datalocation), data = test_post_data1)
		self.assertRedirects(response, self.get_list_url(DataLocation), msg_prefix=msg)
		self.assertObjectUpdated(self.test_dataset_datalocation, 'file_url', 'file_size', 'file_path', 'thumbnail_url', 'offline', msg=msg)
		
		msg = 'The test user may NOT change the dataset of a data location to an other dataset for which he is not a member of the user_group'
		self.client.force_login(self.test_user)
		response = self.client.post(self.get_change_url(self.test_dataset_datalocation), data = test_post_data2)
		self.assertHttpOK(response, msg=msg)
		self.assertFormError(response, 'adminform', 'dataset', ModelChoiceField.default_error_messages['invalid_choice'], msg_prefix=msg)
		
		msg = 'The super user may change the dataset, file_url, file_size, file_path, thumbnail_url, and offline of any data location'
		self.client.force_login(self.super_user)
		response = self.client.post(self.get_change_url(self.test_dataset_datalocation), data = test_post_data2)
		self.assertRedirects(response, self.get_list_url(DataLocation), msg_prefix=msg)
		self.assertObjectUpdated(self.test_dataset_datalocation, 'dataset', 'file_url', 'file_size', 'file_path', 'thumbnail_url', 'offline', msg=msg)
