from django.db import models

from .base_metadata import BaseMetadata

__all__ = ['EitLevel0']

class EitLevel0(BaseMetadata):
	'''Model for the metadata of dataset EIT level 0'''
	
	class Meta(BaseMetadata.Meta):
		verbose_name = 'EIT level 0 metadata'
		verbose_name_plural = 'EIT level 0 metadata'
	
	fits_header = models.TextField(null=True, blank=True)
	blocks_horz = models.IntegerField(verbose_name = 'BLOCKS_HORZ', help_text='', blank=True, null=True)
	blocks_vert = models.IntegerField(verbose_name = 'BLOCKS_VERT', help_text='', blank=True, null=True)
	camera_err = models.TextField(verbose_name = 'CAMERA_ERR', help_text='', blank=True, null=True)
	car_rot = models.FloatField(verbose_name = 'CAR_ROT', help_text='Carrington rotation at earth ', blank=True, null=True)
	ccdtemp = models.FloatField(verbose_name = 'CCDTEMP', help_text='CCD temperature (DN/100) ', blank=True, null=True)
	cdelt1 = models.FloatField(verbose_name = 'CDELT1', help_text='Pixel scale x', blank=True, null=True)
	cdelt2 = models.FloatField(verbose_name = 'CDELT2', help_text='Pixel scale y', blank=True, null=True)
	cftemp = models.FloatField(verbose_name = 'CFTEMP', help_text='CCD cold finger temperature', blank=True, null=True)
	cmp_no = models.IntegerField(verbose_name = 'CMP_NO', help_text='Unique campaign instance (1 = synoptic) ', blank=True, null=True)
	commanded_exposure_time = models.FloatField(verbose_name = 'COMMANDED_EXPOSURE_TIME', help_text='', blank=True, null=True)
	corrected_date_obs = models.DateTimeField(verbose_name = 'CORRECTED_DATE_OBS', help_text='', blank=True, null=True)
	crpix1 = models.FloatField(verbose_name = 'CRPIX1', help_text='Sun center x, EIT pixels', blank=True, null=True)
	crpix2 = models.FloatField(verbose_name = 'CRPIX2', help_text='Sun center y, EIT pixels', blank=True, null=True)
	datasrc = models.TextField(verbose_name = 'DATASRC', help_text='', blank=True, null=True)
	date = models.DateTimeField(verbose_name = 'DATE', help_text='Date of file creation', blank=True, null=True)
	date_obs = models.DateTimeField(verbose_name = 'DATE_OBS', help_text='UTC at spacecraft ', blank=True, null=True)
	expmode = models.TextField(verbose_name = 'EXPMODE', help_text='', blank=True, null=True)
	exptime = models.FloatField(verbose_name = 'EXPTIME', help_text='Exposure time (total commanded + shutter close)', blank=True, null=True)
	filename = models.TextField(verbose_name = 'FILENAME', help_text='', blank=True, null=True)
	filter = models.TextField(verbose_name = 'FILTER', help_text='', blank=True, null=True)
	image_of_seq = models.IntegerField(verbose_name = 'IMAGE_OF_SEQ', help_text='', blank=True, null=True)
	instrume = models.TextField(verbose_name = 'INSTRUME', help_text='', blank=True, null=True)
	leb_proc = models.TextField(verbose_name = 'LEB_PROC', help_text='', blank=True, null=True)
	line_sync = models.TextField(verbose_name = 'LINE_SYNC', help_text='', blank=True, null=True)
	n_missing_blocks = models.IntegerField(verbose_name = 'N_MISSING_BLOCKS', help_text='', blank=True, null=True)
	num_leb_proc = models.IntegerField(verbose_name = 'NUM_LEB_PROC', help_text='', blank=True, null=True)
	object = models.TextField(verbose_name = 'OBJECT', help_text='', blank=True, null=True)
	obs_prog = models.TextField(verbose_name = 'OBS_PROG', help_text='', blank=True, null=True)
	origin = models.TextField(verbose_name = 'ORIGIN', help_text='Rocket Science = NASA GSFC', blank=True, null=True)
	readout_port = models.TextField(verbose_name = 'READOUT_PORT', help_text='', blank=True, null=True)
	sc_roll = models.FloatField(verbose_name = 'SC_ROLL', help_text='s/c roll (Solar north + CCW from nominal)', blank=True, null=True)
	sci_obj = models.TextField(verbose_name = 'SCI_OBJ', help_text='', blank=True, null=True)
	shutter_close_time = models.FloatField(verbose_name = 'SHUTTER_CLOSE_TIME', help_text='', blank=True, null=True)
	solar_b0 = models.FloatField(verbose_name = 'SOLAR_B0', help_text='', blank=True, null=True)
	solar_r = models.FloatField(verbose_name = 'SOLAR_R', help_text='Solar photospheric radius, EIT pixels', blank=True, null=True)
	telescop = models.TextField(verbose_name = 'TELESCOP', help_text='', blank=True, null=True)
	wavelnth = models.IntegerField(verbose_name = 'WAVELNTH', help_text='Wavelength 284 / 171 = Fe IX/X, 195 = Fe XII, / 284 = Fe XV, 304 = He ', blank=True, null=True)
