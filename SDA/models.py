from __future__ import unicode_literals

from django.db import models

class UserProfile(models.Model):
	user=models.OneToOneField(User, db_column='id', primary_key=True, on_delete=models.CASCADE) # related_name="profile"
	description=models.TextField()
	class Meta:
		db_table = 'user_profile'
