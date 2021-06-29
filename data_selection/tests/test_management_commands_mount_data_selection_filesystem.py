import os
import errno
import stat
import subprocess
from pwd import getpwuid
from uuid import uuid4
from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile
from urllib.parse import urljoin
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import F, Func, Value, CharField

from data_selection.management.commands.mount_data_selection_filesystem import DataSelectionFilesystemOperations
from dataset.tests.utils import create_test_dataset


class TestDataSelectionFilesystemOperations(StaticLiveServerTestCase):
	'''Test the DataSelectionFilesystemOperations class'''
	
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		
		# Lookup URL and file content of test files
		cls.test_files = list()
		
		for file_path in ['static/test_file1.fits', 'static/test_file2.fits']:
			file_content = (settings.BASE_DIR / 'dataset/tests' / file_path).read_bytes()
			
			cls.test_files.append({
				'url': urljoin(cls.live_server_url, file_path),
				'content': file_content,
				'size': len(file_content)
			})
	
	def setUp(self):
		# Create test data
		self.test_user = User.objects.create_user(username='test@test.com', email='test@test.com', password='test', first_name='test', last_name='test')
		self.test_dataset = create_test_dataset(name = 'test dataset')
		self.test_data_location1 = self.test_dataset.data_locations.create(file_url = self.test_files[0]['url'], file_size = self.test_files[0]['size'], file_path = 'test_path/file1.fits')
		self.test_data_location2 = self.test_dataset.data_locations.create(file_url = self.test_files[1]['url'], file_size = self.test_files[1]['size'], file_path = 'test_path/file2.fits', offline = True)
		self.test_metadata1 = self.test_dataset.metadata_model.objects.create(oid='test_metadata1', data_location = self.test_data_location1)
		self.test_metadata2 = self.test_dataset.metadata_model.objects.create(oid='test_metadata2', data_location = self.test_data_location2)
		self.test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset, description='test data selection')
		
		# Create an instance of the Operations class
		self.operations = DataSelectionFilesystemOperations(os.geteuid(), os.getegid())
	
	def test_parse_path(self):
		'''Test the parse_path method'''
		
		msg = 'When the path is empty, parse_path must raise a ENOENT OSError'
		path = ''
		with self.assertRaises(OSError, msg=msg) as error:
			self.operations.parse_path(path)
		self.assertEqual(error.exception.errno, errno.ENOENT, msg=msg)
		
		msg = 'When the path is /uuid where the UUID does not correspond to a data selection, parse_path must raise a ENOENT OSError'
		path = '/%s' % uuid4()
		with self.assertRaises(OSError, msg=msg) as error:
			self.operations.parse_path(path)
		self.assertEqual(error.exception.errno, errno.ENOENT, msg=msg)
		
		msg = 'When the path is /uuid/some/path where the UUID does not correspond to a data selection, parse_path must raise a ENOENT OSError'
		path = '/%s/%s' % (uuid4(), 'some/path')
		with self.assertRaises(OSError, msg=msg) as error:
			self.operations.parse_path(path)
		self.assertEqual(error.exception.errno, errno.ENOENT, msg=msg)
		
		msg = 'When the path is /, parse_path must return None for the data_selection and None for the file_path'
		path = '/'
		self.assertEqual(self.operations.parse_path(path), (None, None), msg=msg)
		
		msg = 'When the path is /uuid where the UUID corresponds to a data selection, parse_path must return the data_selection and None for the file_path'
		path = '/%s' % self.test_data_selection.uuid
		self.assertEqual(self.operations.parse_path(path), (self.test_data_selection, None), msg=msg)
		
		msg = 'When the path is /uuid/some/path where the UUID corresponds to a data selection, parse_path must return the data_selection and "some/path" for the file_path'
		path = '/%s/%s' % (self.test_data_selection.uuid, 'some/path')
		self.assertEqual(self.operations.parse_path(path), (self.test_data_selection, 'some/path'), msg=msg)
	
	def test_get_data_location_values(self):
		'''Test the get_data_location_values method'''
		
		msg = 'When data_location_values and extra are empty, get_data_location_values must return a QuerySet with the default values of the online data location'
		data_location_values = []
		extra_values = {}
		result = self.operations.get_data_location_values(self.test_data_selection, *data_location_values, **extra_values)
		self.assertQuerysetEqual(result, [{'file_url': self.test_data_location1.file_url, 'file_size': self.test_data_location1.file_size, 'file_path': self.test_data_location1.file_path, 'thumbnail_url': self.test_data_location1.thumbnail_url, 'update_time': self.test_data_location1.update_time}])
		
		msg = 'When data_location_values specify a value and extra are empty, get_data_location_values must return a QuerySet with only the requested values of the online data location'
		data_location_values = ['file_path']
		extra_values = {}
		result = self.operations.get_data_location_values(self.test_data_selection, *data_location_values, **extra_values)
		self.assertQuerysetEqual(result, [{'file_path': self.test_data_location1.file_path}])
		
		msg = 'When data_location_values specify a value and extra is not empty, get_data_location_values must return a QuerySet with only the requested values of the online data location'
		data_location_values = ['file_path']
		extra_values = {'sub_path': Func(F('file_path'), Value('/'), Value(1), function='SPLIT_PART', output_field=CharField())}
		result = self.operations.get_data_location_values(self.test_data_selection, *data_location_values, **extra_values)
		self.assertQuerysetEqual(result, [{'file_path': self.test_data_location1.file_path, 'sub_path' : self.test_data_location1.file_path.split('/')[0]}])
		
		msg = 'When data_location_values specify a value and extra are empty, get_data_location_values must return a QuerySet with only the requested values of the online data location with a file size smaller than the max'
		self.test_data_location1.file_size = settings.FTP_MAX_FILE_SIZE + 1
		self.test_data_location1.save()
		data_location_values = ['file_path']
		extra_values = {}
		result = self.operations.get_data_location_values(self.test_data_selection, *data_location_values, **extra_values)
		self.assertQuerysetEqual(result, [])
	
	def test_get_data(self):
		'''Test the get_data method'''
		
		msg = 'When the url point to an online file, get_data must return the content of the file at the requested offset and length'
		offset, length = 0, 10
		self.assertEqual(self.operations.get_data(self.test_files[0]['url'], offset, length), self.test_files[0]['content'][offset:offset+length], msg=msg)
		
		msg = 'When the url point to an offline file, get_data must raise an EIO OSError'
		offset, length = 0, 10
		with self.assertRaises(OSError, msg=msg) as error:
			self.operations.get_data(urljoin(self.live_server_url, 'does/not/exist'), offset, length)
		self.assertEqual(error.exception.errno, errno.EIO, msg=msg)
	
	def test_statfs(self):
		'''Test the statfs operation'''
		
		msg = 'statfs must return a dict'
		self.assertIsInstance(self.operations.statfs(None), dict, msg=msg)
	
	def test_getattr(self):
		'''Test the getattr operation'''
		
		msg = 'When the path is /, getattr must return a stat dict for a directory'''
		path = '/'
		result = self.operations.getattr(path)
		self.assertIsInstance(result, dict, msg=msg)
		self.assertTrue(result['st_mode'] & stat.S_IFDIR, msg=msg)
		
		msg = 'When the path is /uuid where the UUID corresponds to a data selection, getattr must return a stat dict for a directory'''
		path = '/%s' % self.test_data_selection.uuid
		result = self.operations.getattr(path)
		self.assertIsInstance(result, dict, msg=msg)
		self.assertTrue(result['st_mode'] & stat.S_IFDIR, msg=msg)
		
		msg = 'When the path is /uuid/dir where the UUID corresponds to a data selection and dir to the beginning of the file_path of a data location, getattr must return a stat dict for a directory'
		path = '/%s/%s' % (self.test_data_selection.uuid, 'test_path')
		result = self.operations.getattr(path)
		self.assertIsInstance(result, dict, msg=msg)
		self.assertTrue(result['st_mode'] & stat.S_IFDIR, msg=msg)
		
		msg = 'When the path is /uuid/dir/file where the UUID corresponds to a data selection and dir/file to the file_path of a data location, getattr must return a stat dict for a file'
		path = '/%s/%s' % (self.test_data_selection.uuid, 'test_path/file1.fits')
		result = self.operations.getattr(path)
		self.assertIsInstance(result, dict, msg=msg)
		self.assertTrue(result['st_mode'] & stat.S_IFREG, msg=msg)
		
		msg = 'When the path is /uuid/dir/file where the UUID corresponds to a data selection and dir/file does not corresponds to the file_path of a data location, getattr must raise a ENOENT OSError'
		path = '/%s/%s' % (self.test_data_selection.uuid, 'does/not/exist.fits')
		with self.assertRaises(OSError, msg=msg) as error:
			self.operations.getattr(path)
		self.assertEqual(error.exception.errno, errno.ENOENT, msg=msg)
	
	def test_readdir(self):
		'''Test the readdir operation'''
		
		# All successfull readdir must return at least these 2
		default_entries = ['.', '..']
		
		msg = 'When the path is /, readdir must return the list of default entries'''
		path = '/'
		result = self.operations.readdir(path)
		self.assertEqual(result, default_entries, msg=msg)
		
		msg = 'When the path is /uuid where the UUID corresponds to a data selection, readdir must return a list of sub directories of the online data location'''
		path = '/%s' % self.test_data_selection.uuid
		result = self.operations.readdir(path)
		self.assertEqual(result, default_entries + ['test_path'], msg=msg)
		
		msg = 'When the path is /uuid/dir where the UUID corresponds to a data selection and dir to the beginning of the file_path of a online data location, readdir must return the file names of the data location'
		path = '/%s/%s' % (self.test_data_selection.uuid, 'test_path')
		result = self.operations.readdir(path)
		self.assertEqual(result, default_entries + ['file1.fits'], msg=msg)
	
	def test_open(self):
		'''Test the open operation'''
		
		msg = 'When the path is /uuid/dir/file where the UUID corresponds to a data selection and dir/file to the file_path of an online data location, and the mode is readonly, open must add the path to the path_urls attribute'
		path = '/%s/%s' % (self.test_data_selection.uuid, self.test_data_location1.file_path)
		self.operations.open(path, os.O_RDONLY)
		self.assertIn(path, self.operations.path_urls, msg=msg)
		
		msg = 'When the path is /uuid/dir/file where the UUID corresponds to a data selection and dir/file to the file_path of an online data location, and the mode is readwrite, open must raise a EACCES OSError'
		path = '/%s/%s' % (self.test_data_selection.uuid, self.test_data_location1.file_path)
		with self.assertRaises(OSError, msg=msg) as error:
			self.operations.open(path, os.O_RDWR)
		self.assertEqual(error.exception.errno, errno.EACCES, msg=msg)
		
		msg = 'When the path is /uuid/dir/file where the UUID corresponds to a data selection and dir/file does not correspond to the file_path of an online data location, and the mode is readonly, open must raise a ENOENT OSError'
		path = '/%s/%s' % (self.test_data_selection.uuid, self.test_data_location2.file_path)
		with self.assertRaises(OSError, msg=msg) as error:
			self.operations.open(path, os.O_RDONLY)
		self.assertEqual(error.exception.errno, errno.ENOENT, msg=msg)
	
	def test_read(self):
		'''Test the read operation'''
		
		msg = 'When the path corresponds to a file that is not opened, read must raise a EBADF OSError'
		path = '/%s/%s' % (self.test_data_selection.uuid, self.test_data_location1.file_path)
		offset, length = 0, 10
		with self.assertRaises(OSError, msg=msg) as error:
			self.operations.read(path, length, offset)
		self.assertEqual(error.exception.errno, errno.EBADF, msg=msg)
		
		msg = 'When the path corresponds to a file that is opened, read must return the content of the file at the requested offset and length'
		path = '/%s/%s' % (self.test_data_selection.uuid, self.test_data_location1.file_path)
		offset, length = 0, 10
		self.operations.open(path, os.O_RDONLY)
		result = self.operations.read(path, length, offset)
		self.assertEqual(result, self.test_files[0]['content'][offset:offset+length], msg=msg)
	
	def test_release(self):
		'''Test the release operation'''
		
		msg = 'When the path corresponds to a file that is not opened, release does nothing'
		path = '/%s/%s' % (self.test_data_selection.uuid, self.test_data_location1.file_path)
		self.assertNotIn(path, self.operations.path_urls, msg=msg)
		self.operations.release(path)
		self.assertNotIn(path, self.operations.path_urls, msg=msg)
		
		msg = 'When the path corresponds to a file that is opened, release must remove the path from the path_urls attribute'
		path = '/%s/%s' % (self.test_data_selection.uuid, self.test_data_location1.file_path)
		self.operations.open(path, os.O_RDONLY)
		self.assertIn(path, self.operations.path_urls, msg=msg)
		self.operations.release(path)
		self.assertNotIn(path, self.operations.path_urls, msg=msg)


class TestMountDataSelectionFilesystemManagementCommand(StaticLiveServerTestCase):
	'''Test the mount_data_selection_filesystem management command'''
	
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		
		# Lookup URL and file content of test files
		cls.test_files = list()
		
		for file_path in ['static/test_file1.fits', 'static/test_file2.fits']:
			file_content = (settings.BASE_DIR / 'dataset/tests' / file_path).read_bytes()
			
			cls.test_files.append({
				'url': urljoin(cls.live_server_url, file_path),
				'content': file_content,
				'size': len(file_content)
			})
		
		cls.user_name = getpwuid(os.geteuid()).pw_name
	
	def setUp(self):
		
		super().setUp()
		
		# Create test data
		self.test_user = User.objects.create_user(username='test@test.com', email='test@test.com', password='test', first_name='test', last_name='test')
		self.test_dataset = create_test_dataset(name = 'test dataset')
		self.test_data_location1 = self.test_dataset.data_locations.create(file_url = self.test_files[0]['url'], file_size = self.test_files[0]['size'], file_path = 'test_path/file1.fits')
		self.test_data_location2 = self.test_dataset.data_locations.create(file_url = self.test_files[1]['url'], file_size = self.test_files[1]['size'], file_path = 'test_path/file2.fits', offline = True)
		self.test_metadata1 = self.test_dataset.metadata_model.objects.create(oid='test_metadata1', data_location = self.test_data_location1)
		self.test_metadata2 = self.test_dataset.metadata_model.objects.create(oid='test_metadata2', data_location = self.test_data_location2)
		self.test_data_selection = self.test_user.data_selections.create(dataset = self.test_dataset, description='test data selection')
		
		# Create the temp mount point and log file, and mount the filesystem
		self.mount_dir = TemporaryDirectory(suffix='.deleteme')
		self.log_file = NamedTemporaryFile(suffix='.deleteme')
		try:
			process = subprocess.run([settings.BASE_DIR / 'manage.py', 'mount_data_selection_filesystem', self.mount_dir.name, '--user', self.user_name, '-l', self.log_file.name , '--verbosity', '2', '--settings', 'project.settings.test'], timeout = 5 * 60, capture_output = True, check = True)
		except subprocess.CalledProcessError as why:
			raise RuntimeError('\n'.join([str(why), why.stderr.decode()])) from why
	
	def tearDown(self):
		super().tearDown()
		
		# Unmount the filesystem, and cleanup the temp mount point and log file
		process = subprocess.run(['fusermount', '-u', self.mount_dir.name], timeout = 5 * 60, capture_output = True)
		self.mount_dir.cleanup()
		self.log_file.close()
	
	def test(self):
		'''Test basic operations on the filesystem'''
		
		root_path = Path(self.mount_dir.name)
		data_location_file_path = root_path / str(self.test_data_selection.uuid) /self.test_data_location1.file_path
		
		msg = 'The root directory must be a mount point'
		self.assertTrue(root_path.is_mount(), msg=msg)
		
		msg = 'The root directory must be empty'
		self.assertEqual(list(root_path.iterdir()), [], msg=msg)
		
		msg = 'The file path of a data locations must be accessible and a file'
		self.assertTrue(data_location_file_path.is_file(), msg=msg)
		
		msg = 'The owner of the directories and files must be the user, and must not have write permission'
		for path in [data_location_file_path, *data_location_file_path.parents]:
			# TODO in python 3.9 use path.is_relative_to(root_path)
			if str(path).startswith(self.mount_dir.name):
				with self.subTest(path=path):
					self.assertEqual(path.owner(), self.user_name, msg=msg)
					self.assertFalse(path.stat().st_mode & os.W_OK, msg=msg)
		
		msg = 'The content of the file must be as expected'
		self.assertEqual(data_location_file_path.read_bytes(), self.test_files[0]['content'], msg=msg)
