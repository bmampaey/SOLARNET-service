from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	'''Allow to add some description to the user'''
	# TODO why do we have this?
	user=models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE) # related_name="profile"
	description=models.TextField()
