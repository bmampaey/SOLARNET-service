import os, pwd, urllib2, urlparse, pytz, logging
from datetime import datetime
from fuse import FUSE, Operations, LoggingMixIn

from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions import Substr
from django.db.models import F, Value

from ..logger import Logger
from data_selection.models import DataSelectionGroup, DataSelection
from dataset.models import Dataset, DataLocation 

def to_system_time(time):
	return (time - datetime(1970, 1, 1, tzinfo = pytz.utc)).total_seconds()

class DataSelectionFilesystem(LoggingMixIn, Operations):
	
	FORBIDDEN_OPEN_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC
	dir_mode = 16749
	file_mode = 33060
	
	def __init__(self, uid, gid, log = logging):
		self.last_fd = 0
		self.fd = dict()
		self.uid = uid
		self.gid = gid
		self.log = log
	
	# Helpers
	# =======
	
	def split_path(self, path):
		file_name, dataset_name, data_selection_group_name, user_id = "","","",""
		while path and path != "/":
			path, tail = os.path.split(path)
			file_name, dataset_name, data_selection_group_name, user_id = dataset_name, data_selection_group_name, user_id, tail
			self.log.debug("file_name %s, dataset_name %s, data_selection_group_name %s, user_id %s", file_name, dataset_name, data_selection_group_name, user_id)
		
		return user_id, data_selection_group_name, dataset_name, file_name
	
	def user_ids(self):
		return DataSelectionGroup.objects.order_by().values_list('user__id', flat=True).distinct()
	
	def data_selection_group_names(self, user_id):
		return DataSelectionGroup.objects.order_by().filter(user__id = user_id).values_list('name', flat=True).distinct()
		
	def dataset_names(self, user_id, data_selection_group_name):
		return DataSelection.objects.order_by().filter(data_selection_group__user__id = user_id, data_selection_group__name=data_selection_group_name).values_list('dataset__name', flat=True).distinct() 
	
	def file_names(self, user_id, data_selection_group_name, dataset_name):
		return self.get_data_locations(user_id, data_selection_group_name, dataset_name).annotate(file_name=Substr(F('file_url'), Value('/([^/]+)$'))).values_list('file_name', flat = True).distinct()
		
	
	def get_data_selection_groups(self, user_id, data_selection_group_name = None):
		if data_selection_group_name:
			return DataSelectionGroup.objects.filter(user__id = user_id, name = data_selection_group_name)
		elif user_id:
			return DataSelectionGroup.objects.filter(user__id = user_id)
		else:
			return DataSelectionGroup.objects.all()
	
	def get_data_selections(self, user_id, data_selection_group_name, dataset_name = None):
		if dataset_name:
			return DataSelection.objects.filter(data_selection_group__user__id = user_id, data_selection_group__name=data_selection_group_name, dataset__name = dataset_name)
		else:
			return DataSelection.objects.filter(data_selection_group__user__id = user_id, data_selection_group__name=data_selection_group_name)
	
	def get_data_locations(self, user_id, data_selection_group_name, dataset_name, file_name = None):
		data_selections = self.get_data_selections(user_id, data_selection_group_name, dataset_name)
		dataset = Dataset.objects.get(name=dataset_name)
		metadata = reduce(lambda a, b: a | b.metadata, data_selections, dataset.metadata_model.objects.none())
		if file_name:
			return DataLocation.objects.filter(**{'file_url__endswith' : '/' + file_name, dataset.metadata_model._meta.app_label + '_metadata__in' : metadata}).order_by().distinct()
		else:
			return DataLocation.objects.filter(**{dataset.metadata_model._meta.app_label + '_metadata__in' : metadata}).order_by().distinct()
	
	def exists(self, path):
		user_id, data_selection_group_name, dataset_name, file_name = self.split_path(path)
		if user_id:
			if data_selection_group_name:
				if dataset_name:
					if file_name:
						return file_name in self.file_names(user_id, data_selection_group_name, dataset_name)
					else:
						return self.get_data_selections(user_id, data_selection_group_name, dataset_name).exists()
				else:
					return self.get_data_selection_groups(user_id, data_selection_group_name).exists()
			else:
				return self.get_data_selection_groups(user_id).exists()
		else:
			return path == '/'
		
		
	
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
	
	def getattr(self, path, fh=None):
		user_id, data_selection_group_name, dataset_name, file_name = self.split_path(path)
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		elif file_name:
			data_location = self.get_data_locations(user_id, data_selection_group_name, dataset_name, file_name = file_name)[0]
			mtime = to_system_time(data_location.updated)
			return {'st_atime': mtime, 'st_ctime': mtime, 'st_gid': self.gid, 'st_mode': self.file_mode, 'st_mtime': mtime, 'st_nlink': 1, 'st_size': data_location.file_size, 'st_uid': self.uid}
		elif dataset_name:
			data_selections = self.get_data_selections(user_id, data_selection_group_name, dataset_name)
			times = [to_system_time(data_selection.created) for data_selection in data_selections]
			return {'st_atime': max(times), 'st_ctime': min(times), 'st_gid': self.gid, 'st_mode': self.dir_mode, 'st_mtime': max(times), 'st_nlink': 2, 'st_size': len(data_selections), 'st_uid': self.uid}
		elif data_selection_group_name:
			data_selection_group = self.get_data_selection_groups(user_id, data_selection_group_name)[0]
			mtime = to_system_time(data_selection_group.updated)
			ctime = to_system_time(data_selection_group.created)
			return {'st_atime': mtime, 'st_ctime': ctime, 'st_gid': self.gid, 'st_mode': self.dir_mode, 'st_mtime': mtime, 'st_nlink': 2, 'st_size': len(data_selection_group.data_selections.all()), 'st_uid': self.uid}
		else:
			data_selection_groups = self.get_data_selection_groups(user_id, data_selection_group_name)
			times = [to_system_time(data_selection_group.created) for data_selection_group in data_selection_groups]
			return {'st_atime': max(times), 'st_ctime': min(times), 'st_gid': self.gid, 'st_mode': self.dir_mode, 'st_mtime': max(times), 'st_nlink': 2, 'st_size': len(data_selection_groups), 'st_uid': self.uid}
	
	def readdir(self, path, fh):
		dirents = ['.', '..']
		user_id, data_selection_group_name, dataset_name, file_name = self.split_path(path)
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		elif file_name:
			raise Exception("Received filename in readdir")
		elif dataset_name:
			return dirents + list(self.file_names(user_id, data_selection_group_name, dataset_name))
		elif data_selection_group_name:
			return dirents + list(self.dataset_names(user_id, data_selection_group_name))
		elif user_id:
			return dirents + list(self.data_selection_group_names(user_id))
		else:
			return dirents + map(str, self.user_ids())
	
	def readlink(self, path):
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		else:
			raise OSError(errno.EINVAL, os.strerror(errno.EINVAL), path)
	
	def mknod(self, path, mode, dev):
		raise OSError(errno.EACCES, os.strerror(errno.EACCES))
	
	def rmdir(self, path):
		user_id, data_selection_group_name, dataset_name, file_name = self.split_path(path)
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		elif file_name:
			raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), path)
		else:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def mkdir(self, path, mode):
		if self.exists(path):
			raise OSError(errno.EEXIST, os.strerror(errno.EEXIST), path)
		else:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def statfs(self, path):
		return os.statvfs(path)
	
	def unlink(self, path):
		user_id, data_selection_group_name, dataset_name, file_name = self.split_path(path)
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		elif not file_name:
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

	def open(self, path, flags):
		#import pdb; pdb.set_trace()
		if flags & self.FORBIDDEN_OPEN_FLAGS:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
		elif not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		elif path not in self.fd:
			user_id, data_selection_group_name, dataset_name, file_name = self.split_path(path)
			data_location = self.get_data_locations(user_id, data_selection_group_name, dataset_name, file_name)[0]
			request = urllib2.urlopen(data_location.file_url)
			self.fd[path] = request.read()
		
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
		
		fuse = FUSE(DataSelectionFilesystem(uid = owner.pw_uid, gid = owner.pw_gid, log = log), options['mountpoint'], foreground=options['foreground'], debug=options['debug'])
