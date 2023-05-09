# Generated by command write_metadata_files version 1
from django.db import models

from .base_metadata import BaseMetadata

__all__ = ['UsetWhiteLightLevel1']

class UsetWhiteLightLevel1(BaseMetadata):
	'''Model for the metadata of dataset USET White Light level 1'''
	
	class Meta(BaseMetadata.Meta):
		verbose_name = 'USET White Light level 1 metadata'
		verbose_name_plural = 'USET White Light level 1 metadata'
	
	fits_header = models.TextField(null=True, blank=True)
	bscale = models.BigIntegerField(verbose_name = 'BSCALE', help_text='To be multiplied to the data array values', blank=True, null=True)
	btype = models.TextField(verbose_name = 'BTYPE', help_text='', blank=True, null=True)
	bunit = models.TextField(verbose_name = 'BUNIT', help_text='', blank=True, null=True)
	bzero = models.BigIntegerField(verbose_name = 'BZERO', help_text='To be added by the data array values', blank=True, null=True)
	camera = models.TextField(verbose_name = 'CAMERA', help_text='', blank=True, null=True)
	cdelt1 = models.FloatField(verbose_name = 'CDELT1', help_text='', blank=True, null=True)
	cdelt2 = models.FloatField(verbose_name = 'CDELT2', help_text='', blank=True, null=True)
	center_x = models.FloatField(verbose_name = 'CENTER_X', help_text='', blank=True, null=True)
	center_y = models.FloatField(verbose_name = 'CENTER_Y', help_text='', blank=True, null=True)
	creator = models.TextField(verbose_name = 'CREATOR', help_text='Name of software that produced the FITS file', blank=True, null=True)
	crota1 = models.FloatField(verbose_name = 'CROTA1', help_text='', blank=True, null=True)
	crota2 = models.FloatField(verbose_name = 'CROTA2', help_text='', blank=True, null=True)
	crpix1 = models.FloatField(verbose_name = 'CRPIX1', help_text='', blank=True, null=True)
	crpix2 = models.FloatField(verbose_name = 'CRPIX2', help_text='', blank=True, null=True)
	crval1 = models.BigIntegerField(verbose_name = 'CRVAL1', help_text='', blank=True, null=True)
	crval2 = models.BigIntegerField(verbose_name = 'CRVAL2', help_text='', blank=True, null=True)
	ctype1 = models.TextField(verbose_name = 'CTYPE1', help_text='Helioproj. westward angle, TAN projection', blank=True, null=True)
	ctype2 = models.TextField(verbose_name = 'CTYPE2', help_text='Helioproj. northward angle, TAN projection', blank=True, null=True)
	cunit1 = models.TextField(verbose_name = 'CUNIT1', help_text='', blank=True, null=True)
	cunit2 = models.TextField(verbose_name = 'CUNIT2', help_text='', blank=True, null=True)
	date = models.DateTimeField(verbose_name = 'DATE', help_text='FITS file creation date', blank=True, null=True)
	date_obs = models.DateTimeField(verbose_name = 'DATE-OBS', help_text='Same value as DATE-BEG', blank=True, null=True)
	extname = models.TextField(verbose_name = 'EXTNAME', help_text='', blank=True, null=True)
	filename = models.TextField(verbose_name = 'FILENAME', help_text='', blank=True, null=True)
	gain = models.BigIntegerField(verbose_name = 'GAIN', help_text='Normalized gain in mili-units', blank=True, null=True)
	instrume = models.TextField(verbose_name = 'INSTRUME', help_text='', blank=True, null=True)
	level = models.BigIntegerField(verbose_name = 'LEVEL', help_text='Data level of fits file', blank=True, null=True)
	naxis = models.BigIntegerField(verbose_name = 'NAXIS', help_text='', blank=True, null=True)
	naxis1 = models.BigIntegerField(verbose_name = 'NAXIS1', help_text='', blank=True, null=True)
	naxis2 = models.BigIntegerField(verbose_name = 'NAXIS2', help_text='', blank=True, null=True)
	obs_hdu = models.BigIntegerField(verbose_name = 'OBS_HDU', help_text='', blank=True, null=True)
	obs_mode = models.TextField(verbose_name = 'OBS_MODE', help_text='Predefined settings used during obs.', blank=True, null=True)
	obsgeo_x = models.BigIntegerField(verbose_name = 'OBSGEO-X', help_text='ECEF X coord of the observer', blank=True, null=True)
	obsgeo_y = models.BigIntegerField(verbose_name = 'OBSGEO-Y', help_text='ECEF Y coord of the observer', blank=True, null=True)
	obsgeo_z = models.BigIntegerField(verbose_name = 'OBSGEO-Z', help_text='ECEF Z coord of the observer', blank=True, null=True)
	obsrvtry = models.TextField(verbose_name = 'OBSRVTRY', help_text='', blank=True, null=True)
	origin = models.TextField(verbose_name = 'ORIGIN', help_text='', blank=True, null=True)
	prstep1 = models.TextField(verbose_name = 'PRSTEP1', help_text='First processing steps', blank=True, null=True)
	solar_p0 = models.FloatField(verbose_name = 'SOLAR_P0', help_text='', blank=True, null=True)
	solar_r = models.FloatField(verbose_name = 'SOLAR_R', help_text='', blank=True, null=True)
	solarnet = models.BigIntegerField(verbose_name = 'SOLARNET', help_text='', blank=True, null=True)
	telescop = models.TextField(verbose_name = 'TELESCOP', help_text='', blank=True, null=True)
	vers_sw = models.DateTimeField(verbose_name = 'VERS_SW', help_text='Version of software applied', blank=True, null=True)
	version = models.FloatField(verbose_name = 'VERSION', help_text='Pipeline version', blank=True, null=True)
	waveunit = models.BigIntegerField(verbose_name = 'WAVEUNIT', help_text='Power of 10 by which the metre is multiplied', blank=True, null=True)
	xposure = models.FloatField(verbose_name = 'XPOSURE', help_text='Total exposure time', blank=True, null=True)
