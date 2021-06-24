from django.db import models

from .base_metadata import BaseMetadata

__all__ = ['Chrotel']

class Chrotel(BaseMetadata):
	azimuth = models.FloatField('AZIMUTH', help_text='telescope azimuth', blank=True, null=True)
	bkpltemp = models.FloatField('BKPLTEMP', help_text='Camera backplane temperature', blank=True, null=True)
	bscale = models.FloatField('BSCALE', help_text='None', blank=True, null=True)
	bunit = models.TextField('BUNIT', help_text='Data is encoded in A/D units', blank=True, null=True)
	bzero = models.IntegerField('BZERO', help_text='Data is Unsigned Integer', blank=True, null=True)
	ccdgain = models.FloatField('CCDGAIN', help_text='CCD gain', blank=True, null=True)
	ccdpress = models.FloatField('CCDPRESS', help_text='CCD chamber pressure', blank=True, null=True)
	ccdtemp = models.FloatField('CCDTEMP', help_text='CCD temperature', blank=True, null=True)
	cdelt1 = models.FloatField('CDELT1', help_text='Plate scale X-axis at CRPIX1', blank=True, null=True)
	cdelt1a = models.FloatField('CDELT1A', help_text='Plate scale X-axis at CRPIX1', blank=True, null=True)
	cdelt1b = models.FloatField('CDELT1B', help_text='Plate scale X-axis at CRPIX1', blank=True, null=True)
	cdelt1c = models.FloatField('CDELT1C', help_text='Plate scale X-axis at CRPIX1', blank=True, null=True)
	cdelt1d = models.FloatField('CDELT1D', help_text='Plate scale X-axis at CRPIX1', blank=True, null=True)
	cdelt1e = models.FloatField('CDELT1E', help_text='Plate scale X-axis at CRPIX1', blank=True, null=True)
	cdelt1f = models.FloatField('CDELT1F', help_text='Plate scale X-axis at CRPIX1', blank=True, null=True)
	cdelt1g = models.FloatField('CDELT1G', help_text='Plate scale X-axis at CRPIX1', blank=True, null=True)
	cdelt2 = models.FloatField('CDELT2', help_text='Plate scale Y-axis at CRPIX2', blank=True, null=True)
	cdelt2a = models.FloatField('CDELT2A', help_text='Plate scale Y-axis at CRPIX2', blank=True, null=True)
	cdelt2b = models.FloatField('CDELT2B', help_text='Plate scale Y-axis at CRPIX2', blank=True, null=True)
	cdelt2c = models.FloatField('CDELT2C', help_text='Plate scale Y-axis at CRPIX2', blank=True, null=True)
	cdelt2d = models.FloatField('CDELT2D', help_text='Plate scale Y-axis at CRPIX2', blank=True, null=True)
	cdelt2e = models.FloatField('CDELT2E', help_text='Plate scale Y-axis at CRPIX2', blank=True, null=True)
	cdelt2f = models.FloatField('CDELT2F', help_text='Plate scale Y-axis at CRPIX2', blank=True, null=True)
	cdelt2g = models.FloatField('CDELT2G', help_text='Plate scale Y-axis at CRPIX2', blank=True, null=True)
	cdrcrev = models.TextField('CDRCREV', help_text='source code revision', blank=True, null=True)
	cdrcvers = models.TextField('CDRCVERS', help_text='data reduction code version', blank=True, null=True)
	content = models.TextField('CONTENT', help_text='None', blank=True, null=True)
	creator = models.TextField('CREATOR', help_text='chrotel data reduction code', blank=True, null=True)
	crln_obs = models.FloatField('CRLN_OBS', help_text='sub-observer carrington longitude', blank=True, null=True)
	crpix1 = models.FloatField('CRPIX1', help_text='Reference pixel X-axis (Disk center)', blank=True, null=True)
	crpix1a = models.FloatField('CRPIX1A', help_text='Reference pixel X-axis (Disk center)', blank=True, null=True)
	crpix1b = models.FloatField('CRPIX1B', help_text='Reference pixel X-axis (Disk center)', blank=True, null=True)
	crpix1c = models.FloatField('CRPIX1C', help_text='Reference pixel X-axis (Disk center)', blank=True, null=True)
	crpix1d = models.FloatField('CRPIX1D', help_text='Reference pixel X-axis (Disk center)', blank=True, null=True)
	crpix1e = models.FloatField('CRPIX1E', help_text='Reference pixel X-axis (Disk center)', blank=True, null=True)
	crpix1f = models.FloatField('CRPIX1F', help_text='Reference pixel X-axis (Disk center)', blank=True, null=True)
	crpix1g = models.FloatField('CRPIX1G', help_text='Reference pixel X-axis (Disk center)', blank=True, null=True)
	crpix2 = models.FloatField('CRPIX2', help_text='Reference pixel Y-axis (Disk center)', blank=True, null=True)
	crpix2a = models.FloatField('CRPIX2A', help_text='Reference pixel Y-axis (Disk center)', blank=True, null=True)
	crpix2b = models.FloatField('CRPIX2B', help_text='Reference pixel Y-axis (Disk center)', blank=True, null=True)
	crpix2c = models.FloatField('CRPIX2C', help_text='Reference pixel Y-axis (Disk center)', blank=True, null=True)
	crpix2d = models.FloatField('CRPIX2D', help_text='Reference pixel Y-axis (Disk center)', blank=True, null=True)
	crpix2e = models.FloatField('CRPIX2E', help_text='Reference pixel Y-axis (Disk center)', blank=True, null=True)
	crpix2f = models.FloatField('CRPIX2F', help_text='Reference pixel Y-axis (Disk center)', blank=True, null=True)
	crpix2g = models.FloatField('CRPIX2G', help_text='Reference pixel Y-axis (Disk center)', blank=True, null=True)
	crval1 = models.FloatField('CRVAL1', help_text='X Coordinate at reference pixel', blank=True, null=True)
	crval1a = models.FloatField('CRVAL1A', help_text='X Coordinate at reference pixel', blank=True, null=True)
	crval1b = models.FloatField('CRVAL1B', help_text='X Coordinate at reference pixel', blank=True, null=True)
	crval1c = models.FloatField('CRVAL1C', help_text='X Coordinate at reference pixel', blank=True, null=True)
	crval1d = models.FloatField('CRVAL1D', help_text='X Coordinate at reference pixel', blank=True, null=True)
	crval1e = models.FloatField('CRVAL1E', help_text='X Coordinate at reference pixel', blank=True, null=True)
	crval1f = models.FloatField('CRVAL1F', help_text='X Coordinate at reference pixel', blank=True, null=True)
	crval1g = models.FloatField('CRVAL1G', help_text='X Coordinate at reference pixel', blank=True, null=True)
	crval2 = models.FloatField('CRVAL2', help_text='Y Coordinate at reference pixel', blank=True, null=True)
	crval2a = models.FloatField('CRVAL2A', help_text='Y Coordinate at reference pixel', blank=True, null=True)
	crval2b = models.FloatField('CRVAL2B', help_text='Y Coordinate at reference pixel', blank=True, null=True)
	crval2c = models.FloatField('CRVAL2C', help_text='Y Coordinate at reference pixel', blank=True, null=True)
	crval2d = models.FloatField('CRVAL2D', help_text='Y Coordinate at reference pixel', blank=True, null=True)
	crval2e = models.FloatField('CRVAL2E', help_text='Y Coordinate at reference pixel', blank=True, null=True)
	crval2f = models.FloatField('CRVAL2F', help_text='Y Coordinate at reference pixel', blank=True, null=True)
	crval2g = models.FloatField('CRVAL2G', help_text='Y Coordinate at reference pixel', blank=True, null=True)
	ctype1 = models.TextField('CTYPE1', help_text='Label X-axis', blank=True, null=True)
	ctype1a = models.TextField('CTYPE1A', help_text='Label X-axis', blank=True, null=True)
	ctype1b = models.TextField('CTYPE1B', help_text='Label X-axis', blank=True, null=True)
	ctype1c = models.TextField('CTYPE1C', help_text='Label X-axis', blank=True, null=True)
	ctype1d = models.TextField('CTYPE1D', help_text='Label X-axis', blank=True, null=True)
	ctype1e = models.TextField('CTYPE1E', help_text='Label X-axis', blank=True, null=True)
	ctype1f = models.TextField('CTYPE1F', help_text='Label X-axis', blank=True, null=True)
	ctype1g = models.TextField('CTYPE1G', help_text='Label X-axis', blank=True, null=True)
	ctype2 = models.TextField('CTYPE2', help_text='Label Y-axis', blank=True, null=True)
	ctype2a = models.TextField('CTYPE2A', help_text='Label Y-axis', blank=True, null=True)
	ctype2b = models.TextField('CTYPE2B', help_text='Label Y-axis', blank=True, null=True)
	ctype2c = models.TextField('CTYPE2C', help_text='Label Y-axis', blank=True, null=True)
	ctype2d = models.TextField('CTYPE2D', help_text='Label Y-axis', blank=True, null=True)
	ctype2e = models.TextField('CTYPE2E', help_text='Label Y-axis', blank=True, null=True)
	ctype2f = models.TextField('CTYPE2F', help_text='Label Y-axis', blank=True, null=True)
	ctype2g = models.TextField('CTYPE2G', help_text='Label Y-axis', blank=True, null=True)
	cunit1 = models.TextField('CUNIT1', help_text='Unit X-axis', blank=True, null=True)
	cunit1a = models.TextField('CUNIT1A', help_text='Unit X-axis', blank=True, null=True)
	cunit1b = models.TextField('CUNIT1B', help_text='Unit X-axis', blank=True, null=True)
	cunit1c = models.TextField('CUNIT1C', help_text='Unit X-axis', blank=True, null=True)
	cunit1d = models.TextField('CUNIT1D', help_text='Unit X-axis', blank=True, null=True)
	cunit1e = models.TextField('CUNIT1E', help_text='Unit X-axis', blank=True, null=True)
	cunit1f = models.TextField('CUNIT1F', help_text='Unit X-axis', blank=True, null=True)
	cunit1g = models.TextField('CUNIT1G', help_text='Unit X-axis', blank=True, null=True)
	cunit2 = models.TextField('CUNIT2', help_text='Unit Y-axis', blank=True, null=True)
	cunit2a = models.TextField('CUNIT2A', help_text='Unit Y-axis', blank=True, null=True)
	cunit2b = models.TextField('CUNIT2B', help_text='Unit Y-axis', blank=True, null=True)
	cunit2c = models.TextField('CUNIT2C', help_text='Unit Y-axis', blank=True, null=True)
	cunit2d = models.TextField('CUNIT2D', help_text='Unit Y-axis', blank=True, null=True)
	cunit2e = models.TextField('CUNIT2E', help_text='Unit Y-axis', blank=True, null=True)
	cunit2f = models.TextField('CUNIT2F', help_text='Unit Y-axis', blank=True, null=True)
	cunit2g = models.TextField('CUNIT2G', help_text='Unit Y-axis', blank=True, null=True)
	darkfile = models.TextField('DARKFILE', help_text='darkframe used for calibration', blank=True, null=True)
	datamax = models.IntegerField('DATAMAX', help_text='max data value', blank=True, null=True)
	datamin = models.IntegerField('DATAMIN', help_text='min data value', blank=True, null=True)
	datavers = models.TextField('DATAVERS', help_text='data format version', blank=True, null=True)
	date = models.DateTimeField('DATE', help_text='UTC time of FITS file creation', blank=True, null=True)
	date_obs = models.DateTimeField('DATE-OBS', help_text='UTC time of observation', blank=True, null=True)
	diskmax = models.IntegerField('DISKMAX', help_text='max data value on solar disk', blank=True, null=True)
	diskmean = models.FloatField('DISKMEAN', help_text='mean data value on solar disk', blank=True, null=True)
	diskmedn = models.FloatField('DISKMEDN', help_text='median data value on solar disk', blank=True, null=True)
	diskmin = models.IntegerField('DISKMIN', help_text='min data value on solar disk', blank=True, null=True)
	diskrms = models.FloatField('DISKRMS', help_text='standard deviation of on-disk data values', blank=True, null=True)
	dsun_obs = models.FloatField('DSUN_OBS', help_text='distance to Sun', blank=True, null=True)
	elevat = models.FloatField('ELEVAT', help_text='telescope elevation', blank=True, null=True)
	exptime = models.FloatField('EXPTIME', help_text='exposure time', blank=True, null=True)
	filename = models.TextField('FILENAME', help_text='name of this data set', blank=True, null=True)
	filter = models.TextField('FILTER', help_text='The used ChroTel bandpass filter', blank=True, null=True)
	filtfwhm = models.FloatField('FILTFWHM', help_text='filter passband FWHM', blank=True, null=True)
	fitsfile = models.TextField('FITSFILE', help_text='name of this data set', blank=True, null=True)
	flatdark = models.TextField('FLATDARK', help_text='flatfield dark used for calibration', blank=True, null=True)
	flatfile = models.TextField('FLATFILE', help_text='flatfield used for calibration', blank=True, null=True)
	glocked = models.IntegerField('GLOCKED', help_text='true if guiding system was locked on sun', blank=True, null=True)
	hgln_obs = models.FloatField('HGLN_OBS', help_text='sub-observer stonyhurst longitude', blank=True, null=True)
	hglt_obs = models.FloatField('HGLT_OBS', help_text='sub-observer heliographic latitude', blank=True, null=True)
	img_rot = models.FloatField('IMG_ROT', help_text='image rotation wrt geocentric north', blank=True, null=True)
	instrume = models.TextField('INSTRUME', help_text='None', blank=True, null=True)
	level = models.TextField('LEVEL', help_text='processing level of this dataset', blank=True, null=True)
	naxis = models.IntegerField('NAXIS', help_text='None', blank=True, null=True)
	naxis1 = models.IntegerField('NAXIS1', help_text='None', blank=True, null=True)
	naxis2 = models.IntegerField('NAXIS2', help_text='None', blank=True, null=True)
	naxis3 = models.IntegerField('NAXIS3', help_text='None', blank=True, null=True)
	object = models.TextField('OBJECT', help_text='None', blank=True, null=True)
	obsnfile = models.TextField('OBSNFILE', help_text='raw observation data', blank=True, null=True)
	origin = models.TextField('ORIGIN', help_text='Kiepenheuer-Institut fuer Sonnenphysik', blank=True, null=True)
	pc1_1 = models.FloatField('PC1_1', help_text='None', blank=True, null=True)
	pc1_1a = models.FloatField('PC1_1A', help_text='None', blank=True, null=True)
	pc1_1b = models.FloatField('PC1_1B', help_text='None', blank=True, null=True)
	pc1_1c = models.FloatField('PC1_1C', help_text='None', blank=True, null=True)
	pc1_1d = models.FloatField('PC1_1D', help_text='None', blank=True, null=True)
	pc1_1e = models.FloatField('PC1_1E', help_text='None', blank=True, null=True)
	pc1_1f = models.FloatField('PC1_1F', help_text='None', blank=True, null=True)
	pc1_1g = models.FloatField('PC1_1G', help_text='None', blank=True, null=True)
	pc1_2 = models.FloatField('PC1_2', help_text='None', blank=True, null=True)
	pc1_2a = models.FloatField('PC1_2A', help_text='None', blank=True, null=True)
	pc1_2b = models.FloatField('PC1_2B', help_text='None', blank=True, null=True)
	pc1_2c = models.FloatField('PC1_2C', help_text='None', blank=True, null=True)
	pc1_2d = models.FloatField('PC1_2D', help_text='None', blank=True, null=True)
	pc1_2e = models.FloatField('PC1_2E', help_text='None', blank=True, null=True)
	pc1_2f = models.FloatField('PC1_2F', help_text='None', blank=True, null=True)
	pc1_2g = models.FloatField('PC1_2G', help_text='None', blank=True, null=True)
	pc2_1 = models.FloatField('PC2_1', help_text='None', blank=True, null=True)
	pc2_1a = models.FloatField('PC2_1A', help_text='None', blank=True, null=True)
	pc2_1b = models.FloatField('PC2_1B', help_text='None', blank=True, null=True)
	pc2_1c = models.FloatField('PC2_1C', help_text='None', blank=True, null=True)
	pc2_1d = models.FloatField('PC2_1D', help_text='None', blank=True, null=True)
	pc2_1e = models.FloatField('PC2_1E', help_text='None', blank=True, null=True)
	pc2_1f = models.FloatField('PC2_1F', help_text='None', blank=True, null=True)
	pc2_1g = models.FloatField('PC2_1G', help_text='None', blank=True, null=True)
	pc2_2 = models.FloatField('PC2_2', help_text='None', blank=True, null=True)
	pc2_2a = models.FloatField('PC2_2A', help_text='None', blank=True, null=True)
	pc2_2b = models.FloatField('PC2_2B', help_text='None', blank=True, null=True)
	pc2_2c = models.FloatField('PC2_2C', help_text='None', blank=True, null=True)
	pc2_2d = models.FloatField('PC2_2D', help_text='None', blank=True, null=True)
	pc2_2e = models.FloatField('PC2_2E', help_text='None', blank=True, null=True)
	pc2_2f = models.FloatField('PC2_2F', help_text='None', blank=True, null=True)
	pc2_2g = models.FloatField('PC2_2G', help_text='None', blank=True, null=True)
	pressure = models.FloatField('PRESSURE', help_text='CCD chamber pressure', blank=True, null=True)
	psd_ll = models.FloatField('PSD_LL', help_text='PSD light level', blank=True, null=True)
	realtime = models.IntegerField('REALTIME', help_text='true if data was processed in realtime mode', blank=True, null=True)
	rot_offs = models.FloatField('ROT_OFFS', help_text='filter specific offset to IMG_ROT', blank=True, null=True)
	rsun_obs = models.FloatField('RSUN_OBS', help_text='apparent radius of solar disk', blank=True, null=True)
	rsun_ref = models.IntegerField('RSUN_REF', help_text='reference radius of the Sun', blank=True, null=True)
	solar_b0 = models.FloatField('SOLAR_B0', help_text='Solar B0 angle', blank=True, null=True)
	solar_p0 = models.FloatField('SOLAR_P0', help_text='Solar P0 angle', blank=True, null=True)
	telescop = models.TextField('TELESCOP', help_text='Chromospheric Telescope', blank=True, null=True)
	temp_bpt = models.FloatField('TEMP_BPT', help_text='Camera backplate temperature', blank=True, null=True)
	temp_ccd = models.FloatField('TEMP_CCD', help_text='CCD temperature', blank=True, null=True)
	tt_rms = models.FloatField('TT_RMS', help_text='Tip-Tilt motion', blank=True, null=True)
	wavelnth = models.FloatField('WAVELNTH', help_text='filter center wavelength', blank=True, null=True)
	wcsname = models.TextField('WCSNAME', help_text='None', blank=True, null=True)
	wcsnamea = models.TextField('WCSNAMEA', help_text='None', blank=True, null=True)
	wcsnameb = models.TextField('WCSNAMEB', help_text='None', blank=True, null=True)
	wcsnamec = models.TextField('WCSNAMEC', help_text='None', blank=True, null=True)
	wcsnamed = models.TextField('WCSNAMED', help_text='None', blank=True, null=True)
	wcsnamee = models.TextField('WCSNAMEE', help_text='None', blank=True, null=True)
	wcsnamef = models.TextField('WCSNAMEF', help_text='None', blank=True, null=True)
	wcsnameg = models.TextField('WCSNAMEG', help_text='None', blank=True, null=True)
