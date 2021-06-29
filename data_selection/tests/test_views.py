from io import BytesIO
from urllib.parse import urljoin
from zipfile import is_zipfile
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from dataset.tests.utils import create_test_dataset

class TestDataSelectionDownloadZipView(StaticLiveServerTestCase):
	'''Test the DataSelectionDownloadZipView view'''
	
	def setUp(self):
		# Create the test data
		self.test_user = User.objects.create_user(username='test@test.com', email='test@test.com', password='test', first_name='test', last_name='test')
		self.test_dataset = create_test_dataset(name = 'test dataset')
		self.test_data_location1 = self.test_dataset.data_locations.create(file_url = urljoin(self.live_server_url, '/static/test_file1.fits'), file_size = 256, file_path = 'test_path1/file.fits')
		self.test_dataset.metadata_model.objects.create(oid='test_metadata1', data_location = self.test_data_location1)
		self.test_dataset.metadata_model.objects.create(oid='test_metadata2')
		self.test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset, description = 'test data selection')
	
	def test_get(self):
		'''Test a GET'''
		
		msg = 'A GET for an existing data selection must return a zip file with appropriate headers'
		url = reverse('data_selection:data_selection_download_zip', kwargs = {'uuid': self.test_data_selection.uuid})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200, msg=msg)
		self.assertEqual(response.headers['Content-Disposition'], "attachment; filename*=utf-8''test_dataset.zip", msg=msg)
		self.assertEqual(response.headers['Content-Type'], 'application/zip', msg=msg)
		self.assertTrue(is_zipfile(BytesIO(b''.join(response.streaming_content))), msg=msg)
		
		msg = 'A GET for an inexisting data selection must return a NotFound response'
		url = reverse('data_selection:data_selection_download_zip', kwargs = {'uuid': '00000000-0000-0000-0000-000000000000'})
		response = self.client.get(url)
		return self.assertEqual(response.status_code, 404, msg=msg)
