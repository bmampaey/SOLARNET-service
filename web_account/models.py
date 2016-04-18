from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now

import uuid
from hashlib import sha1
import hmac

class User(models.Model):
	'''Model for web user, username is replaced by email, there is no password but an api key''' 
	name = models.TextField('Full name of the user')
	email = models.EmailField('Email address', unique = True)
	api_key = models.TextField('API key', blank=True, default='', db_index=True)
	is_active = models.BooleanField('The user is allowed to login', blank = True, null = False, default = True)
	date_joined = models.DateTimeField('Date of user creation', auto_now_add=True)
	last_login = models.DateTimeField('Date of last succesfull login', null = True, blank = True)
	
	def __unicode__(self):
		return unicode(self.email)
	
	def save(self, *args, **kwargs):
			if not self.api_key:
				self.api_key = self.generate_key()
			
			return super(User, self).save(*args, **kwargs)
		
	def generate_key(self):
		# Get a random UUID.
		new_uuid = uuid.uuid4()
		# Hmac that beast.
		return hmac.new(new_uuid.bytes, digestmod=sha1).hexdigest()
	
	def do_login(self):
		self.last_login = now()
		self.save()
		# login is always successful
		return True
	
	def is_authenticated(self):
		return True
	
	def is_anonymous(self):
		return False
	
	def get_username(self):
		return self.email