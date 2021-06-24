from django.db import models

from .base_metadata import BaseMetadata

__all__ = ['Rosa']

class Rosa(BaseMetadata):
	cadence = models.FloatField('CADENCE', help_text='', blank=True, null=True)
	cdelt1 = models.FloatField('CDELT1', help_text='Coordinate increment', blank=True, null=True)
	cdelt2 = models.FloatField('CDELT2', help_text='Coordinate increment', blank=True, null=True)
	channel = models.TextField('CHANNEL', help_text='', blank=True, null=True)
	cunit1 = models.TextField('CUNIT1', help_text='Axis units', blank=True, null=True)
	cunit2 = models.TextField('CUNIT2', help_text='Axis units', blank=True, null=True)
	date = models.TextField('DATE', help_text='Creation UTC (CCCC-MM-DD) date of FITS header', blank=True, null=True)
	extend = models.BigIntegerField('EXTEND', help_text='FITS data may contain extensions', blank=True, null=True)
	goes_cls = models.TextField('GOES_CLS', help_text='', blank=True, null=True)
	instrume = models.TextField('INSTRUME', help_text='', blank=True, null=True)
	naxis = models.BigIntegerField('NAXIS', help_text='Number of data axes', blank=True, null=True)
	naxis1 = models.BigIntegerField('NAXIS1', help_text='', blank=True, null=True)
	naxis2 = models.BigIntegerField('NAXIS2', help_text='', blank=True, null=True)
	obsrvtry = models.TextField('OBSRVTRY', help_text='', blank=True, null=True)
	pointing = models.TextField('POINTING', help_text='', blank=True, null=True)
	solarnet = models.FloatField('SOLARNET', help_text='', blank=True, null=True)
	target = models.TextField('TARGET', help_text='', blank=True, null=True)
	telescop = models.TextField('TELESCOP', help_text='', blank=True, null=True)
	wavelnth = models.FloatField('WAVELNTH', help_text='Central wavelength of filter', blank=True, null=True)
	xposure = models.FloatField('XPOSURE', help_text='Exposure', blank=True, null=True)
