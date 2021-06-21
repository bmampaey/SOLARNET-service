# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-03-16 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0010_remove_grislev1_utime'),
    ]

    operations = [
        migrations.AddField(
            model_name='grislev1',
            name='accumula',
            field=models.BigIntegerField(blank=True, help_text='number of accumulations', null=True, verbose_name='ACCUMULA'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='adunorm',
            field=models.BigIntegerField(blank=True, help_text='normalization factor to ADU', null=True, verbose_name='ADUNORM'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='aosystem',
            field=models.TextField(blank=True, help_text='adaptative optic system', null=True, verbose_name='AOSYSTEM'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='azimut',
            field=models.FloatField(blank=True, help_text='Sun center azimut (degrees)', null=True, verbose_name='AZIMUT'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='b0angle',
            field=models.FloatField(blank=True, help_text='B0 angle (degrees)', null=True, verbose_name='B0ANGLE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='bscale',
            field=models.FloatField(blank=True, help_text='data = pixel * BSCALE + BZERO', null=True, verbose_name='BSCALE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='bzero',
            field=models.FloatField(blank=True, help_text='offset applied to true pixel values', null=True, verbose_name='BZERO'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='camera',
            field=models.TextField(blank=True, help_text='camera', null=True, verbose_name='CAMERA'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='campos',
            field=models.FloatField(blank=True, help_text='camera mirror position (mm)', null=True, verbose_name='CAMPOS'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefi_1',
            field=models.FloatField(blank=True, help_text='coefficient I of state 1', null=True, verbose_name='COEFI-1'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefi_2',
            field=models.FloatField(blank=True, help_text='coefficient I of state 2', null=True, verbose_name='COEFI-2'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefi_3',
            field=models.FloatField(blank=True, help_text='coefficient I of state 3', null=True, verbose_name='COEFI-3'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefi_4',
            field=models.FloatField(blank=True, help_text='coefficient I of state 4', null=True, verbose_name='COEFI-4'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefq_1',
            field=models.FloatField(blank=True, help_text='coefficient Q of state 1', null=True, verbose_name='COEFQ-1'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefq_2',
            field=models.FloatField(blank=True, help_text='coefficient Q of state 2', null=True, verbose_name='COEFQ-2'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefq_3',
            field=models.FloatField(blank=True, help_text='coefficient Q of state 3', null=True, verbose_name='COEFQ-3'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefq_4',
            field=models.FloatField(blank=True, help_text='coefficient Q of state 4', null=True, verbose_name='COEFQ-4'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefu_1',
            field=models.FloatField(blank=True, help_text='coefficient U of state 1', null=True, verbose_name='COEFU-1'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefu_2',
            field=models.FloatField(blank=True, help_text='coefficient U of state 2', null=True, verbose_name='COEFU-2'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefu_3',
            field=models.FloatField(blank=True, help_text='coefficient U of state 3', null=True, verbose_name='COEFU-3'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefu_4',
            field=models.FloatField(blank=True, help_text='coefficient U of state 4', null=True, verbose_name='COEFU-4'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefv_1',
            field=models.FloatField(blank=True, help_text='coefficient V of state 1', null=True, verbose_name='COEFV-1'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefv_2',
            field=models.FloatField(blank=True, help_text='coefficient V of state 2', null=True, verbose_name='COEFV-2'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefv_3',
            field=models.FloatField(blank=True, help_text='coefficient V of state 3', null=True, verbose_name='COEFV-3'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='coefv_4',
            field=models.FloatField(blank=True, help_text='coefficient V of state 4', null=True, verbose_name='COEFV-4'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='colpos',
            field=models.FloatField(blank=True, help_text='collimator mirror position (mm)', null=True, verbose_name='COLPOS'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='datafram',
            field=models.TextField(blank=True, help_text='image portion', null=True, verbose_name='DATAFRAM'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='datavers',
            field=models.BigIntegerField(blank=True, help_text='data version (0 means raw data)', null=True, verbose_name='DATAVERS'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='dec',
            field=models.FloatField(blank=True, help_text='Sun center declination (degrees)', null=True, verbose_name='DEC'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='eimgacc',
            field=models.BigIntegerField(blank=True, help_text='number of extra images to make an accumulation', null=True, verbose_name='EIMGACC'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='elevatio',
            field=models.FloatField(blank=True, help_text='Sun center elevation (degrees)', null=True, verbose_name='ELEVATIO'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='elperadu',
            field=models.BigIntegerField(blank=True, help_text='electrons per adu', null=True, verbose_name='ELPERADU'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='exptime',
            field=models.FloatField(blank=True, help_text='integration time of each image (msec)', null=True, verbose_name='EXPTIME'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='filename',
            field=models.TextField(blank=True, help_text='file name', null=True, verbose_name='FILENAME'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='filestat',
            field=models.TextField(blank=True, help_text='file final status', null=True, verbose_name='FILESTAT'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='fullfram',
            field=models.TextField(blank=True, help_text='original full frame size', null=True, verbose_name='FULLFRAM'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='gratangl',
            field=models.FloatField(blank=True, help_text='grating angle (degrees)', null=True, verbose_name='GRATANGL'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='hourangl',
            field=models.FloatField(blank=True, help_text='Sun center hour angle (degrees)', null=True, verbose_name='HOURANGL'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='ifile',
            field=models.BigIntegerField(blank=True, help_text='file index', null=True, verbose_name='IFILE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='imagtype',
            field=models.TextField(blank=True, help_text='image type', null=True, verbose_name='IMAGTYPE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='irfilter',
            field=models.TextField(blank=True, help_text='camera filter', null=True, verbose_name='IRFILTER'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='iserie',
            field=models.BigIntegerField(blank=True, help_text='serie index', null=True, verbose_name='ISERIE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='l0angle',
            field=models.FloatField(blank=True, help_text='L0 angle (degrees)', null=True, verbose_name='L0ANGLE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='lc1_1',
            field=models.BigIntegerField(blank=True, help_text='state 1 of crystal 1', null=True, verbose_name='LC1-1'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='lc1_2',
            field=models.BigIntegerField(blank=True, help_text='state 2 of crystal 1', null=True, verbose_name='LC1-2'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='lc1_3',
            field=models.BigIntegerField(blank=True, help_text='state 3 of crystal 1', null=True, verbose_name='LC1-3'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='lc1_4',
            field=models.BigIntegerField(blank=True, help_text='state 4 of crystal 1', null=True, verbose_name='LC1-4'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='lc2_1',
            field=models.BigIntegerField(blank=True, help_text='state 1 of crystal 2', null=True, verbose_name='LC2-1'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='lc2_2',
            field=models.BigIntegerField(blank=True, help_text='state 2 of crystal 2', null=True, verbose_name='LC2-2'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='lc2_3',
            field=models.BigIntegerField(blank=True, help_text='state 3 of crystal 2', null=True, verbose_name='LC2-3'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='lc2_4',
            field=models.BigIntegerField(blank=True, help_text='state 4 of crystal 2', null=True, verbose_name='LC2-4'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='lcs',
            field=models.BigIntegerField(blank=True, help_text='number of liquid crystals', null=True, verbose_name='LCS'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='measure',
            field=models.TextField(blank=True, help_text='measure type', null=True, verbose_name='MEASURE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='naxis',
            field=models.BigIntegerField(blank=True, help_text='number of axes', null=True, verbose_name='NAXIS'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='naxis1',
            field=models.BigIntegerField(blank=True, help_text='x', null=True, verbose_name='NAXIS1'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='naxis2',
            field=models.BigIntegerField(blank=True, help_text='lambda', null=True, verbose_name='NAXIS2'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='naxis3',
            field=models.BigIntegerField(blank=True, help_text='number of frames in this file', null=True, verbose_name='NAXIS3'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='nfiles',
            field=models.BigIntegerField(blank=True, help_text='number of split files', null=True, verbose_name='NFILES'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='p0angle',
            field=models.FloatField(blank=True, help_text='P0 angle (degrees)', null=True, verbose_name='P0ANGLE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='paraangl',
            field=models.FloatField(blank=True, help_text='parallactic angle (degrees)', null=True, verbose_name='PARAANGL'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='r0radius',
            field=models.FloatField(blank=True, help_text='solar radius (arcsec)', null=True, verbose_name='R0RADIUS'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='ra',
            field=models.FloatField(blank=True, help_text='Sun center right ascension (degrees)', null=True, verbose_name='RA'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='rotangle',
            field=models.FloatField(blank=True, help_text='rotator angle (degrees)', null=True, verbose_name='ROTANGLE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='rotcode',
            field=models.BigIntegerField(blank=True, help_text='0 means rotator inserted', null=True, verbose_name='ROTCODE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='series',
            field=models.BigIntegerField(blank=True, help_text='number of repetitions of the measure', null=True, verbose_name='SERIES'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='spsystem',
            field=models.TextField(blank=True, help_text='scanning positioner system', null=True, verbose_name='SPSYSTEM'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='states',
            field=models.BigIntegerField(blank=True, help_text='number of modulation states', null=True, verbose_name='STATES'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='stepangl',
            field=models.FloatField(blank=True, help_text='scanning step angle (degrees)', null=True, verbose_name='STEPANGL'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='steps',
            field=models.BigIntegerField(blank=True, help_text='steps of each measure', null=True, verbose_name='STEPS'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='stepsh',
            field=models.BigIntegerField(blank=True, help_text='steps in the axis parallel to the slit', null=True, verbose_name='STEPSH'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='stepsize',
            field=models.FloatField(blank=True, help_text='scanning step size (arcsec)', null=True, verbose_name='STEPSIZE'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='stepsv',
            field=models.BigIntegerField(blank=True, help_text='steps in the axis perpendicular to the slit', null=True, verbose_name='STEPSV'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='telescop',
            field=models.TextField(blank=True, help_text='telescope', null=True, verbose_name='TELESCOP'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='temp_lc1',
            field=models.FloatField(blank=True, help_text='temperature of crystal 1 (C)', null=True, verbose_name='TEMP-LC1'),
        ),
        migrations.AddField(
            model_name='grislev1',
            name='temp_lc2',
            field=models.FloatField(blank=True, help_text='temperature of crystal 2 (C)', null=True, verbose_name='TEMP-LC2'),
        ),
        migrations.AlterField(
            model_name='grislev1',
            name='date_obs',
            field=models.TextField(blank=True, help_text='data acquisition date (yyyy-mm-dd)', null=True, verbose_name='DATE-OBS'),
        ),
        migrations.AlterField(
            model_name='grislev1',
            name='waveleng',
            field=models.BigIntegerField(blank=True, help_text='spectrograph wavelength (nm)', null=True, verbose_name='WAVELENG'),
        ),
    ]
