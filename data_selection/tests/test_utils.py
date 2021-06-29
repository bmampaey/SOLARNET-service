from io import BytesIO
from urllib.parse import urljoin
from zipfile import ZipFile
from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings

from dataset.tests.utils import create_test_dataset
from data_selection.utils import DataSelectionZipIterator


class TestDataSelectionZipIterator(StaticLiveServerTestCase):
	'''Test the DataSelectionZipIterator'''
	
	def setUp(self):
		# Create test data
		self.test_user = User.objects.create_user(username='test@test.com', email='test@test.com', password='test', first_name='test', last_name='test')
		self.test_dataset = create_test_dataset()
		self.test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset, description = 'test data selection')
		self.test_file1_url = urljoin(self.live_server_url, '/static/test_file1.fits')
		self.test_file2_url = urljoin(self.live_server_url, '/static/test_file2.fits')
	
	def assertZipContains(self, zip_iterator, file_paths, missing = False, msg=None):
		'''Ensures that the zip file returned by an iterator contains the files paths and if requested a file called missing_files.txt containig messages about files that could not be included in the archive'''
		zip_file = ZipFile(BytesIO(b''.join(zip_iterator)))
		if not missing:
			self.assertCountEqual(zip_file.namelist(), file_paths, msg=msg)
		else:
			self.assertCountEqual(zip_file.namelist(), file_paths + [settings.ZIP_ARCHIVE_MISSING_FILE_NAME], msg=msg)
			with zip_file.open(settings.ZIP_ARCHIVE_MISSING_FILE_NAME) as f:
				missing_file_content = f.read().decode('UTF-8')
			for message in missing:
				with self.subTest(message = message):
					self.assertIn(message, missing_file_content, msg=msg)
	
	def test_normal_data_selection(self):
		'''Test the iterator with a data selection containing 2 files'''
		
		test_data_location1 = self.test_dataset.data_locations.create(file_url = self.test_file1_url, file_size = 256, file_path = 'test_path1/file.fits')
		test_data_location2 = self.test_dataset.data_locations.create(file_url = self.test_file2_url, file_size = 256, file_path = 'test_path2/file.fits')
		self.test_dataset.metadata_model.objects.create(oid='test_metadata1', data_location = test_data_location1)
		self.test_dataset.metadata_model.objects.create(oid='test_metadata2', data_location = test_data_location2)
		test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset)
		zip_iterator = DataSelectionZipIterator(test_data_selection)
		
		msg = 'When a data selection contains 2 files, the iterator must return a zip file with the corresponding files'
		file_paths = [test_data_location1.file_path, test_data_location2.file_path]
		self.assertZipContains(zip_iterator, file_paths, missing = False, msg=msg)
	
	def test_empty_data_selection(self):
		'''Test the iterator with a data selection containing 0 files'''
		
		test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset)
		zip_iterator = DataSelectionZipIterator(test_data_selection)
		
		msg = 'When a data selection contains no file, the iterator must return an empty zip file'
		file_paths = []
		self.assertZipContains(zip_iterator, file_paths, missing = False, msg=msg)
	
	def test_file_offline(self):
		'''Test the iterator when a file is offline'''
		
		test_data_location1 = self.test_dataset.data_locations.create(file_url = self.test_file1_url, file_size = 256, file_path = 'test_path1/file.fits', offline = False)
		test_data_location2 = self.test_dataset.data_locations.create(file_url = self.test_file2_url, file_size = 256, file_path = 'test_path2/file.fits', offline = True)
		self.test_dataset.metadata_model.objects.create(oid='test_metadata1', data_location = test_data_location1)
		self.test_dataset.metadata_model.objects.create(oid='test_metadata2', data_location = test_data_location2)
		test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset)
		zip_iterator = DataSelectionZipIterator(test_data_selection)
		
		msg = 'When a file is offline, the iterator must return a zip file with a missing file'
		file_paths = [test_data_location1.file_path]
		missing = [test_data_location2.file_path]
		self.assertZipContains(zip_iterator, file_paths, missing = missing, msg=msg)
	
	def test_file_max_size(self):
		'''Test the iterator when a file size is larger than the max'''
		
		test_data_location1 = self.test_dataset.data_locations.create(file_url = self.test_file1_url, file_size = 256, file_path = 'test_path1/file.fits')
		test_data_location2 = self.test_dataset.data_locations.create(file_url = self.test_file2_url, file_size = settings.ZIP_ARCHIVE_MAX_FILE_SIZE + 1, file_path = 'test_path2/file.fits')
		self.test_dataset.metadata_model.objects.create(oid='test_metadata1', data_location = test_data_location1)
		self.test_dataset.metadata_model.objects.create(oid='test_metadata2', data_location = test_data_location2)
		test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset)
		zip_iterator = DataSelectionZipIterator(test_data_selection)
		
		msg = 'When a file size is larger than the max, the iterator must return a zip file with a missing file'
		file_paths = [test_data_location1.file_path]
		missing = [test_data_location2.file_path]
		self.assertZipContains(zip_iterator, file_paths, missing = missing, msg=msg)
	
	@override_settings(ZIP_ARCHIVE_MAX_SIZE=257)
	def test_total_file_size(self):
		'''Test the iterator when the total size of files is larger than the max'''
		
		test_data_location1 = self.test_dataset.data_locations.create(file_url = self.test_file1_url, file_size = 256, file_path = 'test_path1/file.fits')
		test_data_location2 = self.test_dataset.data_locations.create(file_url = self.test_file2_url, file_size = 256, file_path = 'test_path2/file.fits')
		self.test_dataset.metadata_model.objects.create(oid='test_metadata1', date_beg = now(), data_location = test_data_location1)
		self.test_dataset.metadata_model.objects.create(oid='test_metadata2', date_beg = now(), data_location = test_data_location2)
		test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset, query_string='order_by=oid')
		zip_iterator = DataSelectionZipIterator(test_data_selection)
		
		msg = 'When the total size of the files is larger than the max, the iterator must return a zip file with a warning in the missing file'
		file_paths = [test_data_location1.file_path]
		missing = [settings.ZIP_ARCHIVE_TRUNCATED_WARNING]
		self.assertZipContains(zip_iterator, file_paths, missing = missing, msg=msg)
	
	def test_file_not_found(self):
		'''Test the iterator when a file is not found (404)'''
		
		test_data_location1 = self.test_dataset.data_locations.create(file_url = self.test_file1_url, file_size = 256, file_path = 'test_path1/file.fits')
		test_data_location2 = self.test_dataset.data_locations.create(file_url = urljoin(self.live_server_url, '/static/does_not_exist.fits'), file_size = 256, file_path = 'test_path2/file.fits')
		self.test_dataset.metadata_model.objects.create(oid='test_metadata1', data_location = test_data_location1)
		self.test_dataset.metadata_model.objects.create(oid='test_metadata2', data_location = test_data_location2)
		test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset)
		zip_iterator = DataSelectionZipIterator(test_data_selection)
		
		msg = 'When a file cannot be downloaded, the iterator must return a zip file with a missing file'
		file_paths = [test_data_location1.file_path]
		missing = [test_data_location2.file_path]
		self.assertZipContains(zip_iterator, file_paths, missing = missing, msg=msg)
	
	def test_same_path(self):
		'''Test the iterator when 2 matadata share the same data location'''
		
		test_data_location = self.test_dataset.data_locations.create(file_url = self.test_file1_url, file_size = 256, file_path = 'test_path/file.fits')
		self.test_dataset.metadata_model.objects.create(oid='test_metadata1', data_location = test_data_location)
		self.test_dataset.metadata_model.objects.create(oid='test_metadata2', data_location = test_data_location)
		test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset)
		zip_iterator = DataSelectionZipIterator(test_data_selection)
		
		msg = 'When 2 metadata share the same data location, the iterator must return a zip file with a single file'
		file_paths = [test_data_location.file_path]
		self.assertZipContains(zip_iterator, file_paths, missing = False, msg=msg)
