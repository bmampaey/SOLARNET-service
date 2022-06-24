from urllib.parse import urlparse
from django.test import TestCase
from django.contrib.auth.models import User

from dataset.tests.utils import create_test_dataset


class TestDataSelectionModel(TestCase):
	'''Test the DataSelection model'''
	
	def setUp(self):
		# Create test data
		self.test_user = User.objects.create_user(username='test@test.com', email='test@test.com', password='test', first_name='test', last_name='test')
		self.test_dataset = create_test_dataset(name = 'test dataset')
		self.test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset, description='test data selection')
	
	def test_zip_file_name(self):
		'''Test the zip_file_name property'''
		
		msg = 'The zip_file_name property must return a file name corresponding to the dataset name'
		self.assertEqual(self.test_data_selection.zip_file_name, 'test_dataset.zip', msg=msg)
	
	def test_zip_download_url(self):
		'''Test the zip_download_url property'''
		
		msg = 'The zip_download_url property must return a proper HTTPs URL containing the uuid'
		url_parts = urlparse(self.test_data_selection.zip_download_url)
		self.assertEqual('https', url_parts.scheme, msg=msg)
		self.assertTrue(url_parts.netloc, msg=msg)
		self.assertIn('/%s' % self.test_data_selection.uuid, url_parts.path, msg=msg)
	
	def test_ftp_url(self):
		'''Test the ftp_download_url property'''
		
		msg = 'The ftp_download_url property must return a proper FTP URL containing the uuid'
		url_parts = urlparse(self.test_data_selection.ftp_download_url)
		self.assertEqual('ftp', url_parts.scheme, msg=msg)
		self.assertTrue(url_parts.netloc, msg=msg)
		self.assertIn('/%s' % self.test_data_selection.uuid, url_parts.path, msg=msg)
