from django.db import models

from .base_metadata import BaseMetadata

__all__ = ['Rosa']

class Rosa(BaseMetadata):
	'''Model for the metadata of dataset ROSA'''
	
	class Meta(BaseMetadata.Meta):
		verbose_name = 'ROSA'
	
	cadence = models.FloatField(verbose_name = 'CADENCE', help_text='', blank=True, null=True)
	cdelt1 = models.FloatField(verbose_name = 'CDELT1', help_text='Coordinate increment', blank=True, null=True)
	cdelt2 = models.FloatField(verbose_name = 'CDELT2', help_text='Coordinate increment', blank=True, null=True)
	channel = models.TextField(verbose_name = 'CHANNEL', help_text='', blank=True, null=True)
	cunit1 = models.TextField(verbose_name = 'CUNIT1', help_text='Axis units', blank=True, null=True)
	cunit2 = models.TextField(verbose_name = 'CUNIT2', help_text='Axis units', blank=True, null=True)
	date = models.TextField(verbose_name = 'DATE', help_text='Creation UTC (CCCC-MM-DD) date of FITS header', blank=True, null=True)
	extend = models.BigIntegerField(verbose_name = 'EXTEND', help_text='FITS data may contain extensions', blank=True, null=True)
	goes_cls = models.TextField(verbose_name = 'GOES_CLS', help_text='', blank=True, null=True)
	instrume = models.TextField(verbose_name = 'INSTRUME', help_text='', blank=True, null=True)
	naxis = models.BigIntegerField(verbose_name = 'NAXIS', help_text='Number of data axes', blank=True, null=True)
	naxis1 = models.BigIntegerField(verbose_name = 'NAXIS1', help_text='', blank=True, null=True)
	naxis2 = models.BigIntegerField(verbose_name = 'NAXIS2', help_text='', blank=True, null=True)
	obsrvtry = models.TextField(verbose_name = 'OBSRVTRY', help_text='', blank=True, null=True)
	pointing = models.TextField(verbose_name = 'POINTING', help_text='', blank=True, null=True)
	solarnet = models.FloatField(verbose_name = 'SOLARNET', help_text='', blank=True, null=True)
	target = models.TextField(verbose_name = 'TARGET', help_text='', blank=True, null=True)
	telescop = models.TextField(verbose_name = 'TELESCOP', help_text='', blank=True, null=True)
	wavelnth = models.FloatField(verbose_name = 'WAVELNTH', help_text='Central wavelength of filter', blank=True, null=True)
	xposure = models.FloatField(verbose_name = 'XPOSURE', help_text='Exposure', blank=True, null=True)
