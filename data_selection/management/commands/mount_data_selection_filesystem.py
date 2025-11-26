import os
import errno
import stat
import logging
from pwd import getpwnam
from pathlib import PurePosixPath
import requests
from fusepy import FUSE, Operations, FuseOSError
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db.models import Q, F, Func, Value, CharField
from django.db import connection
from django.utils.timezone import now
from django.conf import settings


from data_selection.models import DataSelection
from metadata.utils import get_metadata_queryset

# NOTES:
# - the implementation is based on fusepy https://github.com/fusepy/fusepy
# - and not the ?official? python FUSE library https://github.com/libfuse/python-fuse
# - the choice of errors raised by each operation comes from https://linux.die.net/man/2/
# - most operations are not redefined, and by default raise EROFS (Read-only filesystem)
# - the path argument of the operation methods is always an absolute path and without trailing slash
# - file handles are not used, and therefore can be ignored
# - any method that opens a database connection (i.e. every time a query on a model is done) must close it afterward to avoid many "Idle In Transaction" processes
# see http://stackoverflow.com/questions/1303654/threaded-django-task-doesnt-automatically-handle-transactions-or-db-connections


class DataSelectionFilesystemOperations(Operations):
	'''Operations for FUSE read-only filesystem to read the files of a data selection organized in a tree /data.selection.uuid/data_location.file_path'''
	
	# Filesystem is read-only so files cannot be opened for modification
	FORBIDDEN_OPEN_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC
	
	# Regular files can be read by anyone (permissions r--r--r--)
	FILE_MODE = stat.S_IFREG | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
	
	# Directories can be read and traversed by anyone (permissions r-xr-xr-x)
	DIR_MODE = stat.S_IFDIR | stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
	
	# Directory size in bytes
	DIR_SIZE = 0
	
	# Filesysetm block size
	BLOCK_SIZE = 1024
	
	PATH_SEP = '/'
	
	def __init__(self, uid, gid, debug = False):
		self.uid = uid
		self.gid = gid
		self.debug = debug
		self.log = logging.getLogger('fuse')
		
		# Keep the mount time for the atime, mtime and ctime attributes of the root directory (see getattr)
		self.mount_timestamp = now().timestamp()
		
		# The currently opened file descriptors
		# A dict mapping file paths to file urls
		self.path_urls = dict()
	
	def __call__(self, operation, *args):
		# operation methods are not called directly, but an instance of this class is used as a function via the __call__, e.g to call readdir instance('readdir', '/some/file/path')
		
		# Add logging messages
		if operation not in type(self).__dict__:
			self.log.debug('Operation "%s" is not defined, using default', operation)
		
		self.log.info('%s%r', operation, args)
		try:
			value = super().__call__(operation, *args)
		except OSError as why:
			self.log.info('Raised OSError %s - %s', errno.errorcode[why.errno], os.strerror(why.errno))
			raise
		except Exception as why:
			self.log.error('Raised unexpected exception %s', why, exc_info=True)
			raise
		else:
			if self.log.level >= logging.INFO:
				value_string = repr(value)
				if len(value_string) > 100:
					value_string = value_string[:100] + '[...]'
				self.log.info('Returned %s', value_string)
			return value
		finally:
			# Close the database connection, see notes above
			connection.close()
	
	# Helpers
	
	def parse_path(self, path):
		'''Inspect a path like /uuid/file_path and return the DataSelection instance corresponding to the uuid and the rest of the path as a relative path'''
		
		self.log.debug('parse_path(%r)', path)
		
		data_selection, file_path = None, None
		
		path_parts = PurePosixPath(path).parts
		
		# The path must always be an absolute path
		if not path_parts or path_parts[0] != self.PATH_SEP:
			raise FuseOSError(errno.ENOENT)
		
		# If the path is more than the root directory, then lookup the data selection
		# If the first part of the path is not a proper UUID, a ValidationError will be raised
		# If the data selection does not exists, raise a ENOENT (No such file or directory)
		if len(path_parts) > 1:
			try:
				data_selection = DataSelection.objects.get(uuid = path_parts[1])
			except (DataSelection.DoesNotExist, ValidationError):
				raise FuseOSError(errno.ENOENT)
		
		# If the path is more than the UUID of the data selection, return the rest of the path
		if len(path_parts) > 2:
			file_path = str(PurePosixPath(*path_parts[2:]))
		
		return data_selection, file_path
	
	def get_data_location_values(self, data_selection, *data_location_values, **extra_values):
		'''Return the values of the online data locations related to the metadata of the data selection'''
		
		self.log.debug('get_data_location_values(%r, %r, %r)', data_selection, data_location_values, extra_values)
		
		if not data_location_values:
			data_location_values = ['file_url', 'file_size', 'file_path', 'thumbnail_url', 'update_time']
		
		# Convert the data location values to the foreign key lookup, and add any extra lookup
		values = {value: F('data_location__%s' % value) for value in data_location_values}
		values.update(extra_values)
		
		# If no metadata_content_type has been defined for the dataset, a ValueError will be raised
		try:
			metadata_queryset = get_metadata_queryset(data_selection.dataset.metadata_model, data_selection.query_string, data_selection.owner)
		except ValueError:
			raise FuseOSError(errno.ENOENT)
		
		return metadata_queryset.filter(data_location__offline = False, data_location__file_size__lte = settings.FTP_MAX_FILE_SIZE).values(**values)
	
	def get_data(self, url, offset, length):
		'''Retrieve the content of the file at URL and return the binary data'''
		
		self.log.debug('get_data(%r, %r, %r)', url, offset, length)
		
		# Make a request using the range header to get only what is needed
		# The range header limits are inclusive, so it must be offset + length - 1
		response = requests.get(url, headers = {'Range': 'Bytes=%s-%s' % (offset, offset + length - 1)}, timeout=50)
		
		# If request was successful, return the data as binary, else raise EIO - I/O Error
		# If the status code of the response is "partial_content" (206), the range header was accepted and the response content must correspond to the requested range
		# If the status code of the response is "ok" (200), the range header was NOT accepted and response content must correspond to the whole file, so it must be sliced
		# If the status code of the response is "requested_range_not_satisfiable" (416), the range header was accepted but the offset was beyond the file size, so nothing must be returned
		if response.status_code == requests.codes.partial_content:
			return response.content
		elif response.status_code == requests.codes.ok:
			self.log.info('Range not supported for URL %s', url)
			return response.content[offset:offset+length]
		elif response.status_code == requests.codes.requested_range_not_satisfiable:
			self.log.info('Out of range [%s:%s] for URL %s', offset, offset+length, url)
			return b''
		else:
			self.log.error('Response %s - %s for URL %s', response.status_code, response.reason, url)
			raise FuseOSError(errno.EIO)
	
	# Filesystem operations
	
	def statfs(self, path):
		'''Returns a dictionary with keys identical to the statvfs C structure of statvfs(3)'''
		
		return {
			'f_bsize': self.BLOCK_SIZE, # Filesystem block size
			'f_frsize': self.BLOCK_SIZE, # Fragment size
			'f_blocks': 0, # Size of fs in f_frsize units
			'f_bfree': 0, # Number of free blocks
			'f_bavail': 0, # Number of free blocks for unprivileged users
			'f_files': 1, # Number of inodes
			'f_ffree': 0, # Number of free inodes
			'f_favail': 0, # Number of free inodes for unprivileged users (ignored according to libfuse)
			'f_fsid': 0, # Filesystem ID (ignored according to libfuse)
			'f_flag': 0, # Mount flags (ignored according to libfuse)
			'f_namemax': 255 # Maximum filename length
		}
	
	def getattr(self, path, fh = None):
		'''Returns a dictionary with keys identical to the stat C structure of stat(2)'''
		
		# If the path corresponds only to the root directory (i.e. /) then return stat about the root directory
		# If the path corresponds only to the uuid of a data selection (i.e. /uuid) then return stat about the data selection
		# If the path corresponds to the uuid of a data selection and a file path (i.e. /uuid/file_path) then return stat about the data location that starts with that file_path
		
		stat = {}
		
		data_selection, file_path = self.parse_path(path)
		
		if data_selection is None: # path is /
			# The directory is always shown empty, so the number of hard links is always 2
			# We use the time the filesystem was mounted as the value for the atime, mtime and ctime
			
			stat = {
				'st_mode': self.DIR_MODE, # File type and mode
				'st_nlink': 2, # Number of hard links
				'st_uid': self.uid, # User ID of owner
				'st_gid': self.gid, # Group ID of owner
				'st_size': self.DIR_SIZE, # Total size, in bytes
				'st_atime': self.mount_timestamp, # Time of last access
				'st_mtime': self.mount_timestamp, # Time of last modification
				'st_ctime': self.mount_timestamp, # Time of last status change
			}
		
		elif file_path is None: # path is /uuid
			# The number of hard links is always set as 2, although there can be subdirectories, but looking them up is an expensive database operation
			# We use the data selection creation time as the value for the atime, mtime and ctime
			creation_timestamp = data_selection.creation_time.timestamp()
			
			stat = {
				'st_mode': self.DIR_MODE, # File type and mode
				'st_nlink': 2, # Number of hard links
				'st_uid': self.uid, # User ID of owner
				'st_gid': self.gid, # Group ID of owner
				'st_size': self.DIR_SIZE, # Total size, in bytes
				'st_atime': creation_timestamp, # Time of last access
				'st_mtime': creation_timestamp, # Time of last modification
				'st_ctime': creation_timestamp, # Time of last status change
			}
		
		else: # path is /uuid/file_path
			# The file_path can be either the complete path of a file or only the beginning, in which case it is a directory
			# We use the data location update time as the value for the atime, mtime and ctime, so get the most recent one that starts with file_path
			data_location = self.get_data_location_values(data_selection, 'file_path', 'file_size', 'update_time').filter(Q(file_path__exact = file_path) | Q(file_path__startswith = file_path + self.PATH_SEP)).order_by('-update_time').first()
			
			if data_location is None:
				raise FuseOSError(errno.ENOENT)
			
			elif data_location['file_path'] == file_path: # file_path corresponds to the complete path of a file
				update_timestamp = data_location['update_time'].timestamp()
				file_size = data_location['file_size']
				
				stat = {
					'st_mode': self.FILE_MODE, # File type and mode
					'st_nlink': 1, # Number of hard links
					'st_uid': self.uid, # User ID of owner
					'st_gid': self.gid, # Group ID of owner
					'st_size': file_size, # Total size, in bytes
					'st_atime': update_timestamp, # Time of last access
					'st_mtime': update_timestamp, # Time of last modification
					'st_ctime': update_timestamp, # Time of last status change
				}
			
			else: # file_path corresponds to a subdirectory
				# The number of hard links is always set as 2, although there can be subdirectories, but looking them up is an expensive database operation
				update_timestamp = data_location['update_time'].timestamp()
				
				stat = {
					'st_mode': self.DIR_MODE, # File type and mode
					'st_nlink': 2, # Number of hard links
					'st_uid': self.uid, # User ID of owner
					'st_gid': self.gid, # Group ID of owner
					'st_size': self.DIR_SIZE, # Total size, in bytes
					'st_atime': update_timestamp, # Time of last access
					'st_mtime': update_timestamp, # Time of last modification
					'st_ctime': update_timestamp, # Time of last status change
				}
		
		return stat
	
	def readdir(self, path, fh = None):
		'''Returns a list of the subdirectories and files of path'''
		
		# The list must always include current and parent directory
		dirents = ['.', '..']
		
		data_selection, file_path = self.parse_path(path)
		
		if data_selection is None: # path is /
			# The root directory is always shown empty so that a user can only see the content of a data selection if he knows the UUID
			# In case of debug, return all the UUIDs to simplify debugging
			if self.debug:
				dirents.extend([str(uuid) for uuid in DataSelection.objects.values_list('uuid', flat = True)])
		
		elif file_path is None: # path is /uuid
			# Return the first part of the file_path of all the data locations corresponding to the data selection
			path_part = Func(F('file_path'), Value(self.PATH_SEP), Value(1), function='SPLIT_PART', output_field=CharField())
			data_locations = self.get_data_location_values(data_selection, 'file_path', path_part = path_part)
			dirents += list(data_locations.values_list('path_part', flat=True).distinct())
		
		else: # path is /uuid/file_path
			# file_path must be considered as a directory path (we are doing a readdir)
			# Return the next part of the file_path of all the data locations corresponding to the data selection and that start with the directory_path
			directory_path = file_path + self.PATH_SEP
			parts_count = directory_path.count(self.PATH_SEP) + 1
			path_part = Func(F('file_path'), Value(self.PATH_SEP), Value(parts_count), function='SPLIT_PART', output_field=CharField())
			data_locations = self.get_data_location_values(data_selection, 'file_path', path_part = path_part).filter(file_path__startswith=directory_path)
			dirents += list(data_locations.values_list('path_part', flat=True).distinct())
		
		return dirents
	
	# File operations
	# ============
	
	def open(self, path, flags):
		'''Open a file for reading only'''
		
		# If flags are not compatible for a read-only filesystem, raise a EACCES (Permission denied)
		if flags & self.FORBIDDEN_OPEN_FLAGS:
			raise FuseOSError(errno.EACCES)
		
		# If the file was not already open, lookup the url
		if path not in self.path_urls:
			data_selection, file_path = self.parse_path(path)
			# If data_selection is None or file_path is None, that means the path corresponds to a directory, and reading directories must be done through readdir
			if data_selection is None or file_path is None:
				raise FuseOSError(errno.EACCES)
			
			data_location = self.get_data_location_values(data_selection, 'file_path', 'file_url') .filter(file_path = file_path).first()
			
			if data_location is None:
				raise FuseOSError(errno.ENOENT)
			
			self.path_urls[path] = data_location['file_url']
		
		# Read must return a file handle, but the operations is stateless, so we can just return 0
		# See https://libfuse.github.io/doxygen/structfuse__operations.html#a14b98c3f7ab97cc2ef8f9b1d9dc0709d
		return 0
	
	def read(self, path, length, offset, fh = None):
		'''Read from a file descriptor'''
		
		# If the file is not opened, raise EBADF - Bad file number
		# Else, make the HTTP request for the data
		if path not in self.path_urls:
			raise FuseOSError(errno.EBADF)
		
		return self.get_data(self.path_urls[path], offset, length)
	
	def release(self, path, fh = None):
		'''Release an open file (called when the file is closed by all processes)'''
		self.path_urls.pop(path, None)

class Command(BaseCommand):
	help = 'Mount the pseudo file system of data selections'
	
	def add_arguments(self, parser):
		parser.add_argument('mountpoint', help='The mountpoint for the fuse filesystem.')
		parser.add_argument('--debug', '-d', action='store_true', help='Mount the FUSE filesystem with the "-d" option, and list all the data selections under the root path as /uuid')
		parser.add_argument('--foreground', '-f', action='store_true', help='Mount the FUSE filesystem with the "-f" option (handy for debugging)')
		parser.add_argument('--user', '-u', metavar = 'USERNAME', default='ftp', help='The name of the user that will own the files and directories')
		parser.add_argument('--fsname', default='svo_data_selection', help='The name of the filesystem, for e.g shown when calling the shell command mount')
		parser.add_argument('--logfile', '-l', metavar = 'PATH', help='Path for a log file')
	
	def handle(self, **options):
		
		# Configure logging level depending on verbosity
		root = logging.getLogger()
		
		if options['verbosity'] == 0:
			root.setLevel(logging.ERROR)
		elif options['verbosity'] == 1:
			root.setLevel(logging.WARNING)
		elif options['verbosity'] == 2:
			root.setLevel(logging.INFO)
		else:
			root.setLevel(logging.DEBUG)
		
		# Configure logging handlers
		root.handlers = []
		
		# If running in the foreground, display log messages to console
		if options['foreground']:
			console = logging.StreamHandler()
			console.setFormatter(logging.Formatter(fmt='%(asctime)s.%(msecs)d [%(levelname)s] Thread %(thread)d Function %(module)s.%(funcName)s: %(message)s', datefmt='%H:%M:%S'))
			root.addHandler(console)
		
		# If logfile was requested, write log messages to the file
		if options['logfile']:
			logfile = logging.handlers.WatchedFileHandler(options['logfile'], delay=True)
			logfile.setFormatter(logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s'))
			root.addHandler(logfile)
		
		# Get the passwd entry of the user that will own the files and directories, as to lookup it's uid and gid
		try:
			user = getpwnam(options['user'])
		except KeyError as why:
			raise CommandError('User %s not found' % options['user'])
		
		operations = DataSelectionFilesystemOperations(uid = user.pw_uid, gid = user.pw_gid, debug = options['debug'])
		
		# The filesystem must be mounted with direct_io, else if the size is incorrect, the file will be truncated to the size
		fuse = FUSE(operations, options['mountpoint'], foreground=options['foreground'], debug=options['debug'], nothreads=False, fsname=options['fsname'], direct_io=True, allow_other=True)
