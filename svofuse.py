#!/usr/bin/env python

import logging

import errno
import os
from stat import S_IFDIR, S_IFLNK, S_IFREG
import sys
from time import time
from datetime import datetime
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
import requests, urlparse
import StringIO

# This should go
sys.path.append('/home/benjmam/SOLARNET/SDA')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SDA.settings")
import django
django.setup()

from wizard.models import UserDataSelection, DataSelection
import aia_lev1.views, eit.views, swap.views, hmi_magnetogram

if not hasattr(__builtins__, 'bytes'):
	bytes = str

class HttpFuse(LoggingMixIn, Operations):
	
	FORBIDDEN_OPEN_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC
	
	def __init__(self):
		self.last_fd = 0
		self.fd = dict()
	
	# Helpers
	# =======
	
	def split_path(self, path):
		file_name, dataset_name, selection_name, user_name = "","","",""
		while path and path != "/":
			path, tail = os.path.split(path)
			file_name, dataset_name, selection_name, user_name = dataset_name, selection_name, user_name, tail
			logging.debug("file_name %s, dataset_name %s, selection_name %s, user_name %s", file_name, dataset_name, selection_name, user_name)
		
		return user_name, selection_name, dataset_name, file_name
	
	def user_names(self):
		return UserDataSelection.objects.order_by().values_list('user__username', flat=True).distinct()
	
	def selection_names(self, user_name):
		return UserDataSelection.objects.order_by().filter(user__username = user_name).values_list('name', flat=True).distinct()
		
	def dataset_names(self, user_name, selection_name):
		return DataSelection.objects.order_by().filter(user_data_selection__user__username = user_name, user_data_selection__name=selection_name).values_list('dataset__name', flat=True).distinct() 
	
#	def file_names(self, user_name, selection_name, dataset_name):
#		all_results = set()
#		for data_selection in self.get_data_selections(user_name, selection_name, dataset_name):
#			data_locations = data_selection.dataset.data_location_model.objects.filter(meta_data_id__in=data_selection.data_ids)
#			results = set()
#			for data_location in data_locations:
#				results.add(os.path.basename(urlparse.urlparse(data_location.url).path))
#			all_results.update(results)
#		return all_results
	
	def file_names(self, user_name, selection_name, dataset_name):
		results = set()
		for data_location in self.get_data_locations(user_name, selection_name, dataset_name):
			results.add(os.path.basename(urlparse.urlparse(data_location.url).path))
		return results
	
	def get_user_data_selections(self, user_name, selection_name = None):
		if selection_name:
			return UserDataSelection.objects.filter(user__username = user_name, name = selection_name)
		elif user_name:
			return UserDataSelection.objects.filter(user__username = user_name)
		else:
			return UserDataSelection.objects.filter()
	
	def get_data_selections(self, user_name, selection_name, dataset_name = None):
		if dataset_name:
			return DataSelection.objects.filter(user_data_selection__user__username = user_name, user_data_selection__name=selection_name, dataset__name = dataset_name)
		else:
			return DataSelection.objects.filter(user_data_selection__user__username = user_name, user_data_selection__name=selection_name)
	
	def get_data_locations(self, user_name, selection_name, dataset_name, file_name = None):
		results = set()
		for data_selection in self.get_data_selections(user_name, selection_name, dataset_name):
			data_locations = data_selection.dataset.data_location_model.objects.filter(meta_data_id__in=data_selection.data_ids)
			if file_name:
				results.update(data_locations.filter(url__endswith = '/'+file_name))
			else:
				results.update(data_locations)
		return results
	
	
	def exists(self, path):
		user_name, selection_name, dataset_name, file_name = self.split_path(path)
		if user_name:
			if selection_name:
				if dataset_name:
					if file_name:
						return file_name in self.file_names(user_name, selection_name, dataset_name)
					else:
						return self.get_data_selections(user_name, selection_name, dataset_name).exists()
				else:
					return self.get_user_data_selections(user_name, selection_name).exists()
			else:
				return self.get_user_data_selections(user_name).exists()
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
		#
		user_name, selection_name, dataset_name, file_name = self.split_path(path)
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		elif file_name:
			return {'st_atime': 0, 'st_ctime': 0, 'st_gid': 0, 'st_mode': 33060, 'st_mtime': 0, 'st_nlink': 1, 'st_size': 1073741824, 'st_uid': 0}
		elif dataset_name:
			data_selections = self.get_data_selections(user_name, selection_name, dataset_name)
			times = [(data_selection.created - datetime(1970, 1, 1)).total_seconds() for data_selection in data_selections]
			return {'st_atime': max(times), 'st_ctime': min(times), 'st_gid': 0, 'st_mode': 16749, 'st_mtime': max(times), 'st_nlink': 2, 'st_size': len(data_selections), 'st_uid': 0}
		elif selection_name:
			user_data_selection = self.get_user_data_selections(user_name, selection_name)[0]
			mtime = (user_data_selection.updated - datetime(1970, 1, 1)).total_seconds()
			ctime = (user_data_selection.created - datetime(1970, 1, 1)).total_seconds()
			return {'st_atime': mtime, 'st_ctime': ctime, 'st_gid': 0, 'st_mode': 16749, 'st_mtime': mtime, 'st_nlink': 2, 'st_size': len(user_data_selection.data_selections.all()), 'st_uid': 0}
		else:
			user_data_selections = self.get_user_data_selections(user_name, selection_name)
			times = [(user_data_selection.created - datetime(1970, 1, 1)).total_seconds() for user_data_selection in user_data_selections]
			return {'st_atime': max(times), 'st_ctime': min(times), 'st_gid': 0, 'st_mode': 16749, 'st_mtime': max(times), 'st_nlink': 2, 'st_size': len(user_data_selections), 'st_uid': 0}
	
	def readdir(self, path, fh):
		#
		dirents = ['.', '..']
		user_name, selection_name, dataset_name, file_name = self.split_path(path)
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		elif file_name:
			raise Exception("Received filename in readdir")
		elif dataset_name:
			return dirents + list(self.file_names(user_name, selection_name, dataset_name))
		elif selection_name:
			return dirents + list(self.dataset_names(user_name, selection_name))
		elif user_name:
			return dirents + list(self.selection_names(user_name))
		else:
			return dirents + list(self.user_names())
	
	def readlink(self, path):
		if not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		else:
			raise OSError(errno.EINVAL, os.strerror(errno.EINVAL), path)
	
	def mknod(self, path, mode, dev):
		raise OSError(errno.EACCES, os.strerror(errno.EACCES))
	
	def rmdir(self, path):
		user_name, selection_name, dataset_name, file_name = self.split_path(path)
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
		user_name, selection_name, dataset_name, file_name = self.split_path(path)
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
		if flags & self.FORBIDDEN_OPEN_FLAGS:
			raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
		elif not self.exists(path):
			raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		else:
			user_name, selection_name, dataset_name, file_name = self.split_path(path)
			data_location = self.get_data_locations(user_name, selection_name, dataset_name, file_name).pop()
			self.last_fd += 1
			import pdb; pdb.set_trace()
			request = requests.get(data_location.url)
			self.fd[self.last_fd] = request.content
			return self.last_fd

	def create(self, path, mode, fi=None):
		raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)

	def read(self, path, length, offset, fh):
		return self.fd[fh][offset:offset+length]

	def write(self, path, buf, offset, fh):
		raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)
	
	def truncate(self, path, length, fh=None):
		raise OSError(errno.EACCES, os.strerror(errno.EACCES), path)

	def release(self, path, fh):
		if fh in self.fd:
			del self.fd[fh]


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('usage: %s <mountpoint>' % sys.argv[0])
		sys.exit(1)

	logging.getLogger().setLevel(logging.DEBUG)
	fuse = FUSE(HttpFuse(), sys.argv[1], foreground=True, encoding="ascii")
