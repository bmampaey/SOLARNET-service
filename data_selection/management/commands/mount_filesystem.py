import os, pwd, urlparse, pytz, errno, logging, requests
from datetime import datetime
from functools import wraps

from fuse import FUSE, Operations, LoggingMixIn

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Substr
from django.db.models import Q, F, Value
from django.db import connection

from ..logger import Logger
from web_account.models import User
from data_selection.models import DataSelectionGroup, DataSelection
from dataset.models import Dataset, DataLocation 

def to_system_time(time):
	return (time - datetime(1970, 1, 1, tzinfo = pytz.utc)).total_seconds()

def path_parts(path):
	parts = list()
	while path and path != "/":
		path, tail = os.path.split(path)
		parts.insert(0, tail)
	return parts

def close_connection(func):
	'''Decorator to close the Django database connection at the end'''
	#see http://stackoverflow.com/questions/1303654/threaded-django-task-doesnt-automatically-handle-transactions-or-db-connections
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
		except Exception, why:
			connection.close()
			raise
		else:
			connection.close()
			return result
	
	return wrapper

class HttpBuffer(object):
	'''Very loose HTTP buffer, does not do any verification or buffering'''
	def __init__(self, url):
		self.url = url
	
	def __getitem__(self, arg):
		if not isinstance(arg, slice):
			raise TypeError('list indices must be slice')
		
		response = requests.get(self.url, headers = {'Range': 'Bytes=%s-%s' % (arg.start, arg.stop - 1)}, timeout=50)
		
		if response.status_code in (200, 206):
			return response.content
		else:
			return b''

class DataSelectionFilesystem(LoggingMixIn, Operations):
	
	FORBIDDEN_OPEN_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC
	dir_mode = 16749 # r-xr-xr-x
	file_mode = 33060 # r-xr-xr-x
	
	def __init__(self, uid, gid, log = logging):
		self.last_fd = 0
		self.fd = dict()
		self.uid = uid
		self.gid = gid
		self.log = log
		self.mount_time = to_system_time(datetime.now(pytz.utc))
	
	# Helpers
	# =======
	
	@close_connection
	def split_path(self, path):
		'''Convert a path like /user__id/data_selection_group__name/dataset__name/data_location__file_path to it's associated model instances'''
		user, data_selection_group, dataset, file_path = None, None, None, None
		parts = path_parts(path)
		if parts:
			user__id = parts.pop(0)
			user = User.objects.get(id = user__id)
			if not user.data_selection_groups.exists():
				raise User.DoesNotExist
		if parts:
			data_selection_group__name = parts.pop(0)
			data_selection_group = user.data_selection_groups.get(name = data_selection_group__name)
		if parts:
			dataset__name = parts.pop(0)
			dataset = Dataset.objects.get(name = dataset__name)
			if not data_selection_group.data_selections.filter(dataset__name = dataset__name).exists():
				raise Dataset.DoesNotExist
		if parts:
			file_path = os.path.join(*parts)
		
		return user, data_selection_group, dataset, file_path
	
	@close_connection
	def exists(self, path):
		# Split path raise an error if any part along the path is wrong, except for file_path
		try:
			user, data_selection_group, dataset, file_path = self.split_path(path)
		except ObjectDoesNotExist:
			return False
		# If file_path is None, then it is OK, else we must check that at least one data location with that file_path exists
		if file_path is None:
			return True
		else:
			return data_selection_group.metadata[dataset].filter(Q(data_location__file_path__exact = file_path) | Q(data_location__file_path__startswith = file_path + '/'), data_location__offline=False).exists()
	
	@close_connection
	def is_file(self, path):
		# Split path raise an error if any part along the path is wrong, except for file_path
		try:
			user, data_selection_group, dataset, file_path = self.split_path(path)
		except ObjectDoesNotExist:
			return False
		# If file_path is None, then it is OK, else we must check that at least one data location with that file_path exists
		if file_path is None:
			return True
		else:
			return data_selection_group.metadata[dataset].filter(data_location__file_path = file_path, data_location__offline=False).exists()
	
	
	# Filesystem methods
	# ==================
	
	def access(self, path, mode):
		if self.exists(path):
			return (mode == os.F_OK) or not(os.W_OK & mode) and not(os.X_OK & mode)
		else:
			return False
	
	def chmod(self, path, mode):
		if self.exists(path):
			raise OSError(errno.EPERM, os.strerror(errno.EPERM), path)
		else:
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
	
	def chown(self, path, uid, gid):
		if not isinstance(uid, int) or not isinstance(gid, int):
			raise TypeError("an integer is required")
		elif self.exists(path):
			raise OSError(errno.EPERM, os.strerror(errno.EPERM), path)
		else:
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
	
	@close_connection
	def getattr(self, path, fh=None):
		try:
			user, data_selection_group, dataset, file_path = self.split_path(path)
		except ObjectDoesNotExist:
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		if file_path:
			data_locations = data_selection_group.metadata[dataset].filter(data_location__file_path = file_path, data_location__offline=False).values('data_location__file_size', 'data_location__updated')
			if len(data_locations) > 0: # We have a file
				mtime = to_system_time(data_locations[0]['data_location__updated'])
				file_size = data_locations[0]['data_location__file_size']
				return {'st_atime': mtime, 'st_ctime': mtime, 'st_gid': self.gid, 'st_mode': self.file_mode, 'st_mtime': mtime, 'st_nlink': 1, 'st_size': file_size, 'st_uid': self.uid}
			elif not self.exists(path):
				raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		if data_selection_group:
			mtime = to_system_time(data_selection_group.updated)
			ctime = to_system_time(data_selection_group.created)
			return {'st_atime': mtime, 'st_ctime': ctime, 'st_gid': self.gid, 'st_mode': self.dir_mode, 'st_mtime': mtime, 'st_nlink': 2, 'st_size': 4096, 'st_uid': self.uid}
		elif user:
			times = [to_system_time(data_selection_group.created) for data_selection_group in user.data_selection_groups.all()]
			return {'st_atime': max(times), 'st_ctime': min(times), 'st_gid': self.gid, 'st_mode': self.dir_mode, 'st_mtime': max(times), 'st_nlink': 2, 'st_size': 4096, 'st_uid': self.uid}
		else:
			return {'st_atime': self.mount_time, 'st_ctime': self.mount_time, 'st_gid': self.gid, 'st_mode': self.dir_mode, 'st_mtime': self.mount_time, 'st_nlink': 2, 'st_size': 4096, 'st_uid': self.uid}
	
	@close_connection
	def readdir(self, path, fh):
		dirents = ['.', '..']
		try:
			user, data_selection_group, dataset, file_path = self.split_path(path)
		except ObjectDoesNotExist:
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		
		if file_path:
			# TODO test with a full file path
			# retrieve the good part from file path
			return dirents + list(data_selection_group.metadata[dataset].filter(data_location__file_path__startswith=file_path, data_location__offline=False).annotate(sub_path=Substr(Substr(F('data_location__file_path'), Value(len(file_path) + 1)), Value('^/([^/]+)'))).values_list('sub_path', flat=True).order_by().distinct())
		elif dataset:
			# retrieve the good part from file path
			return dirents + list(data_selection_group.metadata[dataset].filter(data_location__offline=False).annotate(sub_path=Substr(F('data_location__file_path'), Value('^([^/]+)'))).values_list('sub_path', flat=True).order_by().distinct())
		elif data_selection_group:
			return dirents + list(data_selection_group.data_selections.order_by().values_list('dataset__name', flat=True).distinct())
		elif user:
			return dirents + list(user.data_selection_groups.values_list('name', flat=True))
		else:
			return dirents + map(str, DataSelectionGroup.objects.order_by().values_list('user__id', flat=True).distinct())
	
	def readlink(self, path):
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		else:
			raise OSError(errno.EINVAL, os.strerror(errno.EINVAL), path)
	
	def mknod(self, path, mode, dev):
		raise OSError(errno.EACCES, os.strerror(errno.EACCES))
	
	def rmdir(self, path):
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		elif self.is_file(path):
			raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), path)
		else:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def mkdir(self, path, mode):
		if self.exists(path):
			raise OSError(errno.EEXIST, os.strerror(errno.EEXIST), path)
		else:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def statfs(self, path):
		return dict(
			f_bsize=4096,
			f_frsize=4096,
			f_blocks=0,
			f_bfree=0,
			f_bavail=0,
			f_files=1,
			f_ffree=0,
			f_favail=0,
			f_flag=4096, # What?
			f_namemax=255
		)
	
	def unlink(self, path):
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		elif not self.is_file(path):
			raise OSError(errno.EISDIR, os.strerror(errno.EISDIR), path)
		else:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def symlink(self, target, name):
		return os.symlink(target, name)
	
	def rename(self, old, new):
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		else:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def link(self, target, name):
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		else:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def utimens(self, path, times=None):
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		else:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	# File methods
	# ============
	
	@close_connection
	def open(self, path, flags):
		if flags & self.FORBIDDEN_OPEN_FLAGS:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
		elif path not in self.fd:
			try:
				user, data_selection_group, dataset, file_path = self.split_path(path)
			except ObjectDoesNotExist:
				raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
			urls = dataset.metadata_model.objects.filter(data_location__file_path = file_path, data_location__offline=False).values_list('data_location__file_url', flat=True)
			if len(urls) > 0:
				self.fd[path] = HttpBuffer(urls[0])
			else:
				raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		
		self.last_fd += 1
		return self.last_fd
	
	def create(self, path, mode, fi=None):
		raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def read(self, path, length, offset, fh):
		
		return self.fd[path][offset:offset+length]
	
	def write(self, path, buf, offset, fh):
		raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def truncate(self, path, length, fh=None):
		raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def release(self, path, fh):
		if path in self.fd:
			del self.fd[path]

class Command(BaseCommand):
	help = 'Mount the pseudo file system of data selections'
	
	def add_arguments(self, parser):
		parser.add_argument('mountpoint', help='The mountpoint for the fuse filesystem.')
		parser.add_argument('--debug', '-d', default=False, action='store_true', help='Set the logging level to debug')
		parser.add_argument('--foreground', '-f', default=False, action='store_true', help='Run the script in foreground (handy for debugging')
		parser.add_argument('--owner', '-o', default='ftp', help='The user that owns the files.')

	def handle(self, **options):
		
		log = Logger(self, debug = options['debug'])
		try:
			owner = pwd.getpwnam(options['owner'])
		except KeyError, why:
			CommandError('No user %s' % options['owner'])
		
		fuse = FUSE(DataSelectionFilesystem(uid = owner.pw_uid, gid = owner.pw_gid, log = log), options['mountpoint'], foreground=options['foreground'], debug=options['debug'], nothreads=False)
