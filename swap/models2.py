# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Keyword(models.Model):
    column = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=70, blank=True)
    python_type = models.CharField(max_length=12)
    unit = models.CharField(max_length=10, blank=True)
    description = models.CharField(max_length=70, blank=True)

    class Meta:
        managed = False
        db_table = 'keyword'


class MetaData(models.Model):
    filename = models.TextField()
    date_obs = models.DateTimeField(db_column='date-obs', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    wavelnth = models.IntegerField(blank=True, null=True)
    creator = models.TextField(blank=True)
    exptime = models.FloatField(blank=True, null=True)
    level = models.FloatField(blank=True, null=True)
    filepath = models.TextField(blank=True)
    origin = models.TextField(blank=True)
    swavint = models.FloatField(blank=True, null=True)
    pav_rot0 = models.FloatField(blank=True, null=True)
    pav_rot1 = models.FloatField(blank=True, null=True)
    led_sel = models.TextField(blank=True)
    hgln_obs = models.FloatField(blank=True, null=True)
    sacqtime = models.FloatField(blank=True, null=True)
    bitpix = models.IntegerField(blank=True, null=True)
    recoding = models.TextField(blank=True)
    p2_y0 = models.FloatField(blank=True, null=True)
    crval2 = models.FloatField(blank=True, null=True)
    trapelec = models.FloatField(blank=True, null=True)
    crval1 = models.FloatField(blank=True, null=True)
    npreslzw = models.IntegerField(blank=True, null=True)
    cdelt1 = models.FloatField(blank=True, null=True)
    cdelt2 = models.FloatField(blank=True, null=True)
    temp1det = models.FloatField(blank=True, null=True)
    lzwdecor = models.TextField(blank=True)
    los_alt = models.FloatField(blank=True, null=True)
    bscale = models.FloatField(blank=True, null=True)
    temp2det = models.FloatField(blank=True, null=True)
    firstcol = models.IntegerField(blank=True, null=True)
    heey_obs = models.FloatField(blank=True, null=True)
    telescop = models.TextField(blank=True)
    p2_x0 = models.FloatField(blank=True, null=True)
    crota2 = models.FloatField(blank=True, null=True)
    ctype1 = models.TextField(blank=True)
    geod_lon = models.FloatField(blank=True, null=True)
    trantime = models.FloatField(blank=True, null=True)
    geod_alt = models.FloatField(blank=True, null=True)
    heez_obs = models.FloatField(blank=True, null=True)
    led_pow = models.TextField(blank=True)
    solar_ep = models.FloatField(blank=True, null=True)
    bunit = models.TextField(blank=True)
    hglt_obs = models.FloatField(blank=True, null=True)
    swycen = models.FloatField(blank=True, null=True)
    cap_mode = models.TextField(blank=True)
    pga_offs = models.IntegerField(blank=True, null=True)
    filter = models.TextField(blank=True)
    hasstdby = models.IntegerField(blank=True, null=True)
    file_tmr = models.TextField(blank=True)
    last_col = models.IntegerField(blank=True, null=True)
    crpix1 = models.FloatField(blank=True, null=True)
    crpix2 = models.FloatField(blank=True, null=True)
    simple = models.IntegerField(blank=True, null=True)
    bzero = models.FloatField(blank=True, null=True)
    firstrow = models.IntegerField(blank=True, null=True)
    cd2_1 = models.FloatField(blank=True, null=True)
    hasoffst = models.IntegerField(blank=True, null=True)
    cd2_2 = models.FloatField(blank=True, null=True)
    artefx = models.TextField(blank=True)
    wcsname = models.TextField(blank=True)
    naxis1 = models.IntegerField(blank=True, null=True)
    dtplar1 = models.FloatField(blank=True, null=True)
    dtplar2 = models.FloatField(blank=True, null=True)
    naxis2 = models.IntegerField(blank=True, null=True)
    geod_lat = models.FloatField(blank=True, null=True)
    last_row = models.IntegerField(blank=True, null=True)
    pn = models.IntegerField(blank=True, null=True)
    lang_rot = models.FloatField(blank=True, null=True)
    file_raw = models.TextField(blank=True)
    datamax = models.FloatField(blank=True, null=True)
    rsun_arc = models.FloatField(blank=True, null=True)
    hasblack = models.IntegerField(blank=True, null=True)
    gsey_obs = models.FloatField(blank=True, null=True)
    dsun_obs = models.FloatField(blank=True, null=True)
    p2_roll = models.FloatField(blank=True, null=True)
    gsex_obs = models.FloatField(blank=True, null=True)
    gsez_obs = models.FloatField(blank=True, null=True)
    tempdark = models.FloatField(blank=True, null=True)
    datamin = models.FloatField(blank=True, null=True)
    ctype2 = models.TextField(blank=True)
    crota1 = models.FloatField(blank=True, null=True)
    trapprot = models.FloatField(blank=True, null=True)
    is_proc = models.IntegerField(blank=True, null=True)
    heex_obs = models.FloatField(blank=True, null=True)
    lonpole = models.FloatField(blank=True, null=True)
    sizcompi = models.IntegerField(blank=True, null=True)
    swxcen = models.FloatField(blank=True, null=True)
    rebin = models.TextField(blank=True)
    obs_mode = models.TextField(blank=True)
    instrume = models.TextField(blank=True)
    recnum = models.IntegerField(blank=True, null=True)
    detector = models.TextField(blank=True)
    object = models.TextField(blank=True)
    compress = models.TextField(blank=True)
    cunit1 = models.TextField(blank=True)
    cunit2 = models.TextField(blank=True)
    date = models.TextField(blank=True)
    file_tar = models.TextField(blank=True)
    cd1_2 = models.FloatField(blank=True, null=True)
    cd1_1 = models.FloatField(blank=True, null=True)
    recbias = models.IntegerField(blank=True, null=True)
    ttemp1 = models.TextField(blank=True)
    ttemp2 = models.TextField(blank=True)
    readrdiv = models.IntegerField(blank=True, null=True)
    naxis = models.IntegerField(blank=True, null=True)
    eacqtime = models.FloatField(blank=True, null=True)
    nprescr = models.IntegerField(blank=True, null=True)
    pga_gain = models.IntegerField(blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'meta_data'
