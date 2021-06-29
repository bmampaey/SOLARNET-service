from django.test import TestCase
from django.urls import reverse

from dataset.tests.utils import create_test_dataset

class TestDataView(TestCase):
	'''Test the DataView view'''
	
	def setUp(self):
		# Create test data
		self.test_dataset = create_test_dataset()
		self.test_data_location = self.test_dataset.data_locations.create(file_url = '/static/test_file1.fits', file_size = 256, thumbnail_url = '/static/test_thumbnail.png')
		self.test_metadata = self.test_dataset.metadata_model.objects.create(oid='test_metadata', data_location = self.test_data_location)
	
	def test_get(self):
		'''Test a GET'''
		
		msg = 'A GET for a valid dataset and metadata oid must return a redirect response'
		url = reverse('dataset:data', kwargs = {'dataset_name': self.test_dataset.name, 'metadata_oid': self.test_metadata.oid})
		response = self.client.get(url)
		self.assertRedirects(response, self.test_data_location.file_url, msg_prefix=msg)
		
		msg = 'A GET for an invalid dataset must return a NotFound response'
		url = reverse('dataset:data', kwargs = {'dataset_name': 'does_not_exist', 'metadata_oid': self.test_metadata.oid})
		response = self.client.get(url)
		return self.assertEqual(response.status_code, 404, msg=msg)
		
		msg = 'A GET for a valid dataset but invalid oid must return a NotFound response'
		url = reverse('dataset:data', kwargs = {'dataset_name': self.test_dataset.name, 'metadata_oid': 'does_not_exist'})
		response = self.client.get(url)
		return self.assertEqual(response.status_code, 404, msg=msg)


class TestThumbnailView(TestCase):
	'''Test the ThumbnailView view'''
	
	def setUp(self):
		# Create test data
		self.test_dataset = create_test_dataset()
		self.test_data_location = self.test_dataset.data_locations.create(file_url = '/static/test_file1.fits', file_size = 256, thumbnail_url = '/static/test_thumbnail.png')
		self.test_metadata = self.test_dataset.metadata_model.objects.create(oid='test_metadata', data_location = self.test_data_location)
	
	def test_get(self):
		'''Test a GET'''
		
		msg = 'A GET for a valid dataset and metadata oid must return a redirect response'
		url = reverse('dataset:thumbnail', kwargs = {'dataset_name': self.test_dataset.name, 'metadata_oid': self.test_metadata.oid})
		response = self.client.get(url)
		self.assertRedirects(response, self.test_data_location.thumbnail_url, msg_prefix=msg)
		
		msg = 'A GET for an invalid dataset must return a NotFound response'
		url = reverse('dataset:thumbnail', kwargs = {'dataset_name': 'does_not_exist', 'metadata_oid': self.test_metadata.oid})
		response = self.client.get(url)
		return self.assertEqual(response.status_code, 404, msg=msg)
		
		msg = 'A GET for a valid dataset but invalid oid must return a NotFound response'
		url = reverse('dataset:thumbnail', kwargs = {'dataset_name': self.test_dataset.name, 'metadata_oid': 'does_not_exist'})
		response = self.client.get(url)
		return self.assertEqual(response.status_code, 404, msg=msg)
