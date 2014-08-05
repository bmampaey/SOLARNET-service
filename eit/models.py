from __future__ import unicode_literals

from django.db import models
import SDA.models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.


class MetaData(models.Model):
	id = models.BigIntegerField(primary_key=True)
	filename = models.CharField(max_length=18, blank=True)
	date_obs = models.DateTimeField(blank=True, null=True)
	corrected_date_obs = models.DateTimeField(blank=True, null=True)
	wavelnth = models.IntegerField(blank=True, null=True)
	exptime = models.FloatField(blank=True, null=True)
	n_missing_blocks = models.IntegerField(blank=True, null=True)
	origin = models.CharField(max_length=14, blank=True)
	instrume = models.CharField(max_length=3, blank=True)
	crpix1 = models.FloatField(blank=True, null=True)
	crpix2 = models.FloatField(blank=True, null=True)
	cdelt1 = models.FloatField(blank=True, null=True)
	cdelt2 = models.FloatField(blank=True, null=True)
	object = models.CharField(max_length=18, blank=True)
	commanded_exposure_time = models.CharField(max_length=9, blank=True)
	expmode = models.CharField(max_length=9, blank=True)
	num_leb_proc = models.IntegerField(blank=True, null=True)
	image_of_seq = models.IntegerField(blank=True, null=True)
	cmp_no = models.IntegerField(blank=True, null=True)
	car_rot = models.FloatField(blank=True, null=True)
	sc_roll = models.FloatField(blank=True, null=True)
	ccdtemp = models.FloatField(blank=True, null=True)
	leb_proc = models.CharField(max_length=25, blank=True)
	obs_prog = models.CharField(max_length=40, blank=True)
	cftemp = models.FloatField(blank=True, null=True)
	solar_r = models.FloatField(blank=True, null=True)
	solar_b0 = models.FloatField(blank=True, null=True)
	blocks_horz = models.IntegerField(blank=True, null=True)
	blocks_vert = models.IntegerField(blank=True, null=True)
	line_sync = models.CharField(max_length=2, blank=True)
	telescop = models.CharField(max_length=4, blank=True)
	datasrc = models.CharField(max_length=18, blank=True)
	readout_port = models.CharField(max_length=1, blank=True)
	camera_err = models.CharField(max_length=3, blank=True)
	filter = models.CharField(max_length=6, blank=True)
	shutter_close_time = models.CharField(max_length=8, blank=True)
	sci_obj = models.CharField(max_length=30, blank=True)
	date = models.DateTimeField(blank=True, null=True)
	
	class Meta:
		managed = True
		db_table = 'meta_data'


class Keyword(SDA.models.Keyword):
	
	class Meta(SDA.models.Keyword.Meta):
		pass


class DataLocation(SDA.models.DataLocation):
	id = models.OneToOneField(MetaData, primary_key=True, db_column = "id", on_delete=models.CASCADE)
	
	class Meta(SDA.models.DataLocation.Meta):
		pass
