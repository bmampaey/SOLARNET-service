from __future__ import unicode_literals
from django.db import models
from .base import BaseMetadata

class Crisp(BaseMetadata):
	ao_lock = models.FloatField('AO_LOCK', help_text='Fraction of time the AO was locking, 2s average', blank=True, null=True)
	ao_nmode = models.BigIntegerField('AO_NMODE', help_text='Number of AO corrected Mirror modes', blank=True, null=True)
	atmos_r0 = models.FloatField('ATMOS_R0', help_text='Atmospheric coherence length (mean value)', blank=True, null=True)
	btype = models.TextField('BTYPE', help_text='Type of data in array', blank=True, null=True)
	bunit = models.TextField('BUNIT', help_text='Units in array', blank=True, null=True)
	cadavg = models.FloatField('CADAVG', help_text='Average of actual cadence', blank=True, null=True)
	cadmax = models.FloatField('CADMAX', help_text='Maximum of actual cadence', blank=True, null=True)
	cadmin = models.FloatField('CADMIN', help_text='Minimum of actual cadence', blank=True, null=True)
	cadvar = models.FloatField('CADVAR', help_text='Variance of actual cadence', blank=True, null=True)
	camera = models.TextField('CAMERA', help_text='', blank=True, null=True)
	cdelt1 = models.BigIntegerField('CDELT1', help_text='Unity transform', blank=True, null=True)
	cdelt1a = models.FloatField('CDELT1A', help_text='Zero FOV extent', blank=True, null=True)
	cdelt2 = models.BigIntegerField('CDELT2', help_text='Unity transform', blank=True, null=True)
	cdelt2a = models.FloatField('CDELT2A', help_text='Zero FOV extent', blank=True, null=True)
	cdelt3 = models.BigIntegerField('CDELT3', help_text='Unity transform', blank=True, null=True)
	cdelt4 = models.BigIntegerField('CDELT4', help_text='Stokes indices [1,2,3,4] --> [I,Q,U,V]', blank=True, null=True)
	cdelt5 = models.BigIntegerField('CDELT5', help_text='Unity transform', blank=True, null=True)
	cname1 = models.TextField('CNAME1', help_text='', blank=True, null=True)
	cname2 = models.TextField('CNAME2', help_text='', blank=True, null=True)
	cname3 = models.TextField('CNAME3', help_text='', blank=True, null=True)
	cname5 = models.TextField('CNAME5', help_text='', blank=True, null=True)
	crpix1 = models.BigIntegerField('CRPIX1', help_text='Unity transform', blank=True, null=True)
	crpix1a = models.FloatField('CRPIX1A', help_text='Center pixel of image array', blank=True, null=True)
	crpix2 = models.BigIntegerField('CRPIX2', help_text='Unity transform', blank=True, null=True)
	crpix2a = models.FloatField('CRPIX2A', help_text='Center pixel of image array', blank=True, null=True)
	crpix3 = models.BigIntegerField('CRPIX3', help_text='Unity transform', blank=True, null=True)
	crpix4 = models.BigIntegerField('CRPIX4', help_text='Index of Stokes components in pixel 1', blank=True, null=True)
	crpix5 = models.BigIntegerField('CRPIX5', help_text='Unity transform', blank=True, null=True)
	crval1 = models.BigIntegerField('CRVAL1', help_text='Unity transform', blank=True, null=True)
	crval1a = models.FloatField('CRVAL1A', help_text='Coordinates of center of image array', blank=True, null=True)
	crval2 = models.BigIntegerField('CRVAL2', help_text='Unity transform', blank=True, null=True)
	crval2a = models.FloatField('CRVAL2A', help_text='Coordinates of center of image array', blank=True, null=True)
	crval3 = models.BigIntegerField('CRVAL3', help_text='Unity transform', blank=True, null=True)
	crval4 = models.BigIntegerField('CRVAL4', help_text='The first Stokes index is 1', blank=True, null=True)
	crval5 = models.BigIntegerField('CRVAL5', help_text='Unity transform', blank=True, null=True)
	csyer1 = models.BigIntegerField('CSYER1', help_text='Orientation unknown', blank=True, null=True)
	csyer2 = models.BigIntegerField('CSYER2', help_text='Orientation unknown', blank=True, null=True)
	ctype1 = models.TextField('CTYPE1', help_text='SOLAR X', blank=True, null=True)
	ctype2 = models.TextField('CTYPE2', help_text='SOLAR Y', blank=True, null=True)
	ctype3 = models.TextField('CTYPE3', help_text='Wavelength, function of tuning and scan number', blank=True, null=True)
	ctype4 = models.TextField('CTYPE4', help_text='Stokes vector [I,Q,U,V]', blank=True, null=True)
	ctype5 = models.TextField('CTYPE5', help_text='Time, function of tuning and scan number', blank=True, null=True)
	cunit1 = models.TextField('CUNIT1', help_text='Unit along axis 1', blank=True, null=True)
	cunit2 = models.TextField('CUNIT2', help_text='Unit along axis 2', blank=True, null=True)
	cunit3 = models.TextField('CUNIT3', help_text='Wavelength unit, tabulated for dim. 3 and 5', blank=True, null=True)
	cunit5 = models.TextField('CUNIT5', help_text='', blank=True, null=True)
	cwdis3 = models.TextField('CWDIS3', help_text='WAVE distortions in lookup table', blank=True, null=True)
	cwerr3 = models.FloatField('CWERR3', help_text='Max total distortion', blank=True, null=True)
	datakurt = models.FloatField('DATAKURT', help_text='The excess kurtosis of the data (provided value', blank=True, null=True)
	datamax = models.FloatField('DATAMAX', help_text='The maximum data value (provided value)', blank=True, null=True)
	datamean = models.FloatField('DATAMEAN', help_text='The average data value (provided value)', blank=True, null=True)
	datamedn = models.FloatField('DATAMEDN', help_text='The 50 percentile of the data (provided value)', blank=True, null=True)
	datamin = models.FloatField('DATAMIN', help_text='The minimum data value (provided value)', blank=True, null=True)
	datap01 = models.FloatField('DATAP01', help_text='The 01 percentile of the data (provided value)', blank=True, null=True)
	datap10 = models.FloatField('DATAP10', help_text='The 10 percentile of the data (provided value)', blank=True, null=True)
	datap25 = models.FloatField('DATAP25', help_text='The 25 percentile of the data (provided value)', blank=True, null=True)
	datap75 = models.FloatField('DATAP75', help_text='The 75 percentile of the data (provided value)', blank=True, null=True)
	datap90 = models.FloatField('DATAP90', help_text='The 90 percentile of the data (provided value)', blank=True, null=True)
	datap95 = models.FloatField('DATAP95', help_text='The 95 percentile of the data (provided value)', blank=True, null=True)
	datap98 = models.FloatField('DATAP98', help_text='The 98 percentile of the data (provided value)', blank=True, null=True)
	datap99 = models.FloatField('DATAP99', help_text='The 99 percentile of the data (provided value)', blank=True, null=True)
	datarms = models.FloatField('DATARMS', help_text='The RMS deviation from the mean (provided value', blank=True, null=True)
	dataskew = models.FloatField('DATASKEW', help_text='The skewness of the data (provided value)', blank=True, null=True)
	date = models.TextField('DATE', help_text='Creation UTC date of FITS header', blank=True, null=True)
	date_avg = models.DateTimeField('DATE-AVG', help_text='Average time of observation (provided va', blank=True, null=True)
	date_obs = models.DateTimeField('DATE-OBS', help_text='Inferred from directory.', blank=True, null=True)
	dateref = models.TextField('DATEREF', help_text='Reference time in ISO-8601', blank=True, null=True)
	detector = models.TextField('DETECTOR', help_text='', blank=True, null=True)
	dw3_apply = models.FloatField('DW3.APPLY', help_text='Application stage (world coordinates)', blank=True, null=True)
	dw3_associate = models.FloatField('DW3.ASSOCIATE', help_text='Association stage (pixel coordinates)', blank=True, null=True)
	dw3_axis1 = models.BigIntegerField('DW3 AXIS1', help_text='Spatial X', blank=True, null=True)
	dw3_axis_1 = models.FloatField('DW3.AXIS.1', help_text='Spatial X', blank=True, null=True)
	dw3_axis2 = models.BigIntegerField('DW3 AXIS2', help_text='Spatial Y', blank=True, null=True)
	dw3_axis_2 = models.FloatField('DW3.AXIS.2', help_text='Spatial Y', blank=True, null=True)
	dw3_axis3 = models.BigIntegerField('DW3 AXIS3', help_text='Scan number', blank=True, null=True)
	dw3_axis_3 = models.FloatField('DW3.AXIS.3', help_text='Scan number', blank=True, null=True)
	dw3_cwdis_lookup = models.FloatField('DW3.CWDIS.LOOKUP', help_text='Distortions in lookup table', blank=True, null=True)
	dw3_cwerr = models.FloatField('DW3 CWERR', help_text='Max distortion (this correction step)', blank=True, null=True)
	dw3_extver = models.FloatField('DW3.EXTVER', help_text='Extension version number', blank=True, null=True)
	dw3_name = models.TextField('DW3 NAME', help_text='Type of correction', blank=True, null=True)
	dw3_naxes = models.BigIntegerField('DW3 NAXES', help_text='3 axes in the lookup table', blank=True, null=True)
	elev_ang = models.FloatField('ELEV_ANG', help_text='Elevation angle (mean value)', blank=True, null=True)
	extend = models.BigIntegerField('EXTEND', help_text='The file has extension(s).', blank=True, null=True)
	filename = models.TextField('FILENAME', help_text='', blank=True, null=True)
	filled = models.BigIntegerField('FILLED', help_text='Missing pixels have been filled.', blank=True, null=True)
	filter1 = models.TextField('FILTER1', help_text='Inferred from filename.', blank=True, null=True)
	fnumsum = models.TextField('FNUMSUM', help_text='List of frame numbers in the sum', blank=True, null=True)
	instrume = models.TextField('INSTRUME', help_text='Name of instrument', blank=True, null=True)
	longstrn = models.TextField('LONGSTRN', help_text='The OGIP long string convention may be used.', blank=True, null=True)
	naxis = models.BigIntegerField('NAXIS', help_text='Number of data axes', blank=True, null=True)
	naxis1 = models.BigIntegerField('NAXIS1', help_text='Number of positions along axis 1', blank=True, null=True)
	naxis2 = models.BigIntegerField('NAXIS2', help_text='Number of positions along axis 2', blank=True, null=True)
	naxis3 = models.BigIntegerField('NAXIS3', help_text='Number of positions along axis 3', blank=True, null=True)
	naxis4 = models.BigIntegerField('NAXIS4', help_text='Number of positions along axis 4', blank=True, null=True)
	naxis5 = models.BigIntegerField('NAXIS5', help_text='Number of positions along axis 5', blank=True, null=True)
	npixels = models.BigIntegerField('NPIXELS', help_text='Number of pixels (provided value)', blank=True, null=True)
	nsumexp = models.FloatField('NSUMEXP', help_text='Number of summed exposures (median value)', blank=True, null=True)
	object = models.TextField('OBJECT', help_text='', blank=True, null=True)
	observer = models.TextField('OBSERVER', help_text='', blank=True, null=True)
	obsgeo_x = models.BigIntegerField('OBSGEO-X', help_text='SST location', blank=True, null=True)
	obsgeo_y = models.BigIntegerField('OBSGEO-Y', help_text='SST location', blank=True, null=True)
	obsgeo_z = models.BigIntegerField('OBSGEO-Z', help_text='SST location', blank=True, null=True)
	obs_hdu = models.BigIntegerField('OBS_HDU', help_text='', blank=True, null=True)
	obsrvtry = models.TextField('OBSRVTRY', help_text='Name of observatory', blank=True, null=True)
	pc1_1 = models.FloatField('PC1_1', help_text='No rotations', blank=True, null=True)
	pc2_2 = models.FloatField('PC2_2', help_text='No rotations', blank=True, null=True)
	pc3_3 = models.FloatField('PC3_3', help_text='No rotations', blank=True, null=True)
	pc4_4 = models.FloatField('PC4_4', help_text='No rotations', blank=True, null=True)
	pc5_5 = models.FloatField('PC5_5', help_text='No rotations', blank=True, null=True)
	prbra1 = models.TextField('PRBRA1', help_text='Version control branch', blank=True, null=True)
	prbra2 = models.TextField('PRBRA2', help_text='Version control branch', blank=True, null=True)
	prbra3 = models.TextField('PRBRA3', help_text='Version control branch', blank=True, null=True)
	prbra4 = models.TextField('PRBRA4', help_text='Version control branch', blank=True, null=True)
	prbra5 = models.TextField('PRBRA5', help_text='Version control branch', blank=True, null=True)
	prbra6 = models.TextField('PRBRA6', help_text='Version control branch', blank=True, null=True)
	prlib1 = models.TextField('PRLIB1', help_text='Software library', blank=True, null=True)
	prlib1a = models.TextField('PRLIB1A', help_text='Additional software library', blank=True, null=True)
	prlib1b = models.TextField('PRLIB1B', help_text='Additional software library', blank=True, null=True)
	prlib1c = models.TextField('PRLIB1C', help_text='Additional software library', blank=True, null=True)
	prlib1d = models.TextField('PRLIB1D', help_text='Additional software library', blank=True, null=True)
	prlib1e = models.TextField('PRLIB1E', help_text='Additional software library', blank=True, null=True)
	prlib2 = models.TextField('PRLIB2', help_text='Software library containing red::make_wb_cube', blank=True, null=True)
	prlib2a = models.TextField('PRLIB2A', help_text='Additional software library', blank=True, null=True)
	prlib2b = models.TextField('PRLIB2B', help_text='Additional software library', blank=True, null=True)
	prlib2c = models.TextField('PRLIB2C', help_text='Additional software library', blank=True, null=True)
	prlib2d = models.TextField('PRLIB2D', help_text='Additional software library', blank=True, null=True)
	prlib3 = models.TextField('PRLIB3', help_text='Software library containing crisp::demodulate', blank=True, null=True)
	prlib3a = models.TextField('PRLIB3A', help_text='Additional software library', blank=True, null=True)
	prlib3b = models.TextField('PRLIB3B', help_text='Additional software library', blank=True, null=True)
	prlib3c = models.TextField('PRLIB3C', help_text='Additional software library', blank=True, null=True)
	prlib3d = models.TextField('PRLIB3D', help_text='Additional software library', blank=True, null=True)
	prlib4 = models.TextField('PRLIB4', help_text='Software library containing crisp::make_nb_cube', blank=True, null=True)
	prlib4a = models.TextField('PRLIB4A', help_text='Additional software library', blank=True, null=True)
	prlib4b = models.TextField('PRLIB4B', help_text='Additional software library', blank=True, null=True)
	prlib4c = models.TextField('PRLIB4C', help_text='Additional software library', blank=True, null=True)
	prlib4d = models.TextField('PRLIB4D', help_text='Additional software library', blank=True, null=True)
	prlib5 = models.TextField('PRLIB5', help_text='Software library containing red::fitscube_cross', blank=True, null=True)
	prlib5a = models.TextField('PRLIB5A', help_text='Additional software library', blank=True, null=True)
	prlib5b = models.TextField('PRLIB5B', help_text='Additional software library', blank=True, null=True)
	prlib5c = models.TextField('PRLIB5C', help_text='Additional software library', blank=True, null=True)
	prlib5d = models.TextField('PRLIB5D', help_text='Additional software library', blank=True, null=True)
	prlib6 = models.TextField('PRLIB6', help_text='Software library containing red::fitscube_expor', blank=True, null=True)
	prlib6a = models.TextField('PRLIB6A', help_text='Additional software library', blank=True, null=True)
	prlib6b = models.TextField('PRLIB6B', help_text='Additional software library', blank=True, null=True)
	prlib6c = models.TextField('PRLIB6C', help_text='Additional software library', blank=True, null=True)
	prlib6d = models.TextField('PRLIB6D', help_text='Additional software library', blank=True, null=True)
	prmode1 = models.TextField('PRMODE1', help_text='Processing mode', blank=True, null=True)
	prmode3 = models.TextField('PRMODE3', help_text='Processing mode', blank=True, null=True)
	prmode4 = models.TextField('PRMODE4', help_text='Processing mode', blank=True, null=True)
	prmode5 = models.TextField('PRMODE5', help_text='Processing mode', blank=True, null=True)
	prmode6 = models.TextField('PRMODE6', help_text='Processing mode', blank=True, null=True)
	prpara1 = models.TextField('PRPARA1', help_text='List of parameters/options for PRPROC1', blank=True, null=True)
	prpara2 = models.TextField('PRPARA2', help_text='List o', blank=True, null=True)
	prpara3 = models.TextField('PRPARA3', help_text='List of parameters/options for PRPROC2', blank=True, null=True)
	prpara4 = models.TextField('PRPARA4', help_text='List of parameters/options for PRPROC4', blank=True, null=True)
	prpara6 = models.TextField('PRPARA6', help_text='List of parameters/options for PRPROC6', blank=True, null=True)
	prproc2 = models.TextField('PRPROC2', help_text='Name of procedure used', blank=True, null=True)
	prproc3 = models.TextField('PRPROC3', help_text='Name of procedure used', blank=True, null=True)
	prproc4 = models.TextField('PRPROC4', help_text='Name of procedure used', blank=True, null=True)
	prproc5 = models.TextField('PRPROC5', help_text='Name of procedure used', blank=True, null=True)
	prproc6 = models.TextField('PRPROC6', help_text='Name of procedure used', blank=True, null=True)
	prstep1 = models.TextField('PRSTEP1', help_text='Processing step name', blank=True, null=True)
	prstep2 = models.TextField('PRSTEP2', help_text='Processing step name', blank=True, null=True)
	prstep3 = models.TextField('PRSTEP3', help_text='Processing step name', blank=True, null=True)
	prstep4 = models.TextField('PRSTEP4', help_text='Processing step name', blank=True, null=True)
	prstep5 = models.TextField('PRSTEP5', help_text='Processing step name', blank=True, null=True)
	prstep6 = models.TextField('PRSTEP6', help_text='Processing step name', blank=True, null=True)
	prver1 = models.TextField('PRVER1', help_text='Library version/MJD of last update', blank=True, null=True)
	prver1a = models.TextField('PRVER1A', help_text='Library version/MJD of last update', blank=True, null=True)
	prver1b = models.TextField('PRVER1B', help_text='Library version/MJD of last update', blank=True, null=True)
	prver1c = models.TextField('PRVER1C', help_text='Library version/MJD of last update', blank=True, null=True)
	prver1d = models.TextField('PRVER1D', help_text='Library version/MJD of last update', blank=True, null=True)
	prver1e = models.TextField('PRVER1E', help_text='Library version/MJD of last update (From .momfb', blank=True, null=True)
	prver2 = models.TextField('PRVER2', help_text='Library version/MJD of last update', blank=True, null=True)
	prver2a = models.TextField('PRVER2A', help_text='Library version/MJD of last update', blank=True, null=True)
	prver2b = models.TextField('PRVER2B', help_text='Library version/MJD of last update', blank=True, null=True)
	prver2c = models.TextField('PRVER2C', help_text='Library version/MJD of last update', blank=True, null=True)
	prver2d = models.TextField('PRVER2D', help_text='Library version/MJD of last update', blank=True, null=True)
	prver3 = models.TextField('PRVER3', help_text='Library version/MJD of last update', blank=True, null=True)
	prver3a = models.TextField('PRVER3A', help_text='Library version/MJD of last update', blank=True, null=True)
	prver3b = models.TextField('PRVER3B', help_text='Library version/MJD of last update', blank=True, null=True)
	prver3c = models.TextField('PRVER3C', help_text='Library version/MJD of last update', blank=True, null=True)
	prver3d = models.TextField('PRVER3D', help_text='Library version/MJD of last update', blank=True, null=True)
	prver4 = models.TextField('PRVER4', help_text='Library version/MJD of last update', blank=True, null=True)
	prver4a = models.TextField('PRVER4A', help_text='Library version/MJD of last update', blank=True, null=True)
	prver4b = models.TextField('PRVER4B', help_text='Library version/MJD of last update', blank=True, null=True)
	prver4c = models.TextField('PRVER4C', help_text='Library version/MJD of last update', blank=True, null=True)
	prver4d = models.TextField('PRVER4D', help_text='Library version/MJD of last update', blank=True, null=True)
	prver5 = models.TextField('PRVER5', help_text='Library version/MJD of last update', blank=True, null=True)
	prver5a = models.TextField('PRVER5A', help_text='Library version/MJD of last update', blank=True, null=True)
	prver5b = models.TextField('PRVER5B', help_text='Library version/MJD of last update', blank=True, null=True)
	prver5c = models.TextField('PRVER5C', help_text='Library version/MJD of last update', blank=True, null=True)
	prver5d = models.TextField('PRVER5D', help_text='Library version/MJD of last update', blank=True, null=True)
	prver6 = models.TextField('PRVER6', help_text='Library version/MJD of last update', blank=True, null=True)
	prver6a = models.TextField('PRVER6A', help_text='Library version/MJD of last update', blank=True, null=True)
	prver6b = models.TextField('PRVER6B', help_text='Library version/MJD of last update', blank=True, null=True)
	prver6c = models.TextField('PRVER6C', help_text='Library version/MJD of last update', blank=True, null=True)
	prver6d = models.TextField('PRVER6D', help_text='Library version/MJD of last update', blank=True, null=True)
	ps1_0 = models.TextField('PS1_0', help_text='EXTNAME; EXTVER=EXTLEVEL=1 is default', blank=True, null=True)
	ps1_1 = models.TextField('PS1_1', help_text='TTYPE for column w/coordinates', blank=True, null=True)
	ps1_2 = models.TextField('PS1_2', help_text='TTYPE for INDEX', blank=True, null=True)
	ps2_0 = models.TextField('PS2_0', help_text='EXTNAME; EXTVER=EXTLEVEL=1 is default', blank=True, null=True)
	ps2_1 = models.TextField('PS2_1', help_text='TTYPE for column w/coordinates', blank=True, null=True)
	ps2_2 = models.TextField('PS2_2', help_text='TTYPE for INDEX', blank=True, null=True)
	ps3_0 = models.TextField('PS3_0', help_text='EXTNAME; EXTVER=EXTLEVEL=1 is default', blank=True, null=True)
	ps3_1 = models.TextField('PS3_1', help_text='TTYPE for column w/coordinates', blank=True, null=True)
	ps5_0 = models.TextField('PS5_0', help_text='EXTNAME; EXTVER=EXTLEVEL=1 is default', blank=True, null=True)
	ps5_1 = models.TextField('PS5_1', help_text='TTYPE for column w/coordinates', blank=True, null=True)
	pv1_3 = models.BigIntegerField('PV1_3', help_text='Coord. 1 tabulated coordinate number', blank=True, null=True)
	pv2_3 = models.BigIntegerField('PV2_3', help_text='Coord. 2 tabulated coordinate number', blank=True, null=True)
	pv3_3 = models.BigIntegerField('PV3_3', help_text='Coord. 3 tabulated coordinate number', blank=True, null=True)
	pv5_3 = models.BigIntegerField('PV5_3', help_text='Coord. 5 tabulated coordinate number', blank=True, null=True)
	release = models.TextField('RELEASE', help_text='', blank=True, null=True)
	releasec = models.TextField('RELEASEC', help_text='', blank=True, null=True)
	requestr = models.TextField('REQUESTR', help_text='', blank=True, null=True)
	scannum = models.BigIntegerField('SCANNUM', help_text='Scan number (first value)', blank=True, null=True)
	solarnet = models.FloatField('SOLARNET', help_text='Fully SOLARNET-compliant=1.0, partially=0.5', blank=True, null=True)
	startobs = models.DateTimeField('STARTOBS', help_text='', blank=True, null=True)
	telconfg = models.TextField('TELCONFG', help_text='Telescope configuration', blank=True, null=True)
	telescop = models.TextField('TELESCOP', help_text='Name of telescope', blank=True, null=True)
	texposur = models.FloatField('TEXPOSUR', help_text='Single-exposure time (median value)', blank=True, null=True)
	timesys = models.TextField('TIMESYS', help_text='', blank=True, null=True)
	var_keys = models.TextField('VAR_KEYS', help_text='SOLARNET variable-keywords', blank=True, null=True)
	waveband = models.TextField('WAVEBAND', help_text='', blank=True, null=True)
	wavelnth = models.FloatField('WAVELNTH', help_text='Prefilter peak wavelength', blank=True, null=True)
	waveunit = models.BigIntegerField('WAVEUNIT', help_text='WAVELNTH in units 10^WAVEUNIT m = nm', blank=True, null=True)
	wcsnamea = models.TextField('WCSNAMEA', help_text='', blank=True, null=True)
	xposure = models.FloatField('XPOSURE', help_text='Summed exposure times (median value)', blank=True, null=True)
