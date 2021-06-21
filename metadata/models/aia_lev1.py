
from django.db import models
from .base import BaseMetadata

class AiaLev1(BaseMetadata):
	acs_cgt = models.TextField('ACS_CGT', help_text='ACS ID of Controlling Guide Telescope - ACS_AN_NUM_CGT', blank=True, null=True)
	acs_eclp = models.TextField('ACS_ECLP', help_text='ACS eclipse flag - ACS_AN_FLAG_CSS_ECLIPSE', blank=True, null=True)
	acs_mode = models.TextField('ACS_MODE', help_text='ACS pointing mode - ACS_AN_ACS_MODE', blank=True, null=True)
	acs_safe = models.TextField('ACS_SAFE', help_text='ACS safe hold flag - ACS_AN_FLAG_ACE_INSAFEHOLD', blank=True, null=True)
	acs_sunp = models.TextField('ACS_SUNP', help_text='ACS sun presense flag - ACS_AN_FLAG_DSS_SUNPRES', blank=True, null=True)
	aecdelay = models.IntegerField('AECDELAY', help_text='AIA_IMG_AEC_DELAY', blank=True, null=True)
	aecmode = models.TextField('AECMODE', help_text='AIA_IMG_AEC_MODE', blank=True, null=True)
	aectype = models.IntegerField('AECTYPE', help_text='AIA_IMG_AEC_TYPE', blank=True, null=True)
	agt1svy = models.IntegerField('AGT1SVY', help_text='AIA_GT1_SUNVECTOR_Y', blank=True, null=True)
	agt1svz = models.IntegerField('AGT1SVZ', help_text='AIA_GT1_SUNVECTOR_Z', blank=True, null=True)
	agt2svy = models.IntegerField('AGT2SVY', help_text='AIA_GT2_SUNVECTOR_Y', blank=True, null=True)
	agt2svz = models.IntegerField('AGT2SVZ', help_text='AIA_GT2_SUNVECTOR_Z', blank=True, null=True)
	agt3svy = models.IntegerField('AGT3SVY', help_text='AIA_GT3_SUNVECTOR_Y', blank=True, null=True)
	agt3svz = models.IntegerField('AGT3SVZ', help_text='AIA_GT3_SUNVECTOR_Z', blank=True, null=True)
	agt4svy = models.IntegerField('AGT4SVY', help_text='AIA_GT4_SUNVECTOR_Y', blank=True, null=True)
	agt4svz = models.IntegerField('AGT4SVZ', help_text='AIA_GT4_SUNVECTOR_Z', blank=True, null=True)
	aiaecenf = models.IntegerField('AIAECENF', help_text='AIA_IMG_AEC_ENA_FLAG', blank=True, null=True)
	aiaecti = models.IntegerField('AIAECTI', help_text='AIA_IMG_AEC_TABLE_ID', blank=True, null=True)
	aiagp1 = models.IntegerField('AIAGP1', help_text='AIA_IMG_GP1', blank=True, null=True)
	aiagp10 = models.IntegerField('AIAGP10', help_text='AIA_IMG_GP10', blank=True, null=True)
	aiagp2 = models.IntegerField('AIAGP2', help_text='AIA_IMG_GP2', blank=True, null=True)
	aiagp3 = models.IntegerField('AIAGP3', help_text='AIA_IMG_GP3', blank=True, null=True)
	aiagp4 = models.IntegerField('AIAGP4', help_text='AIA_IMG_GP4', blank=True, null=True)
	aiagp5 = models.IntegerField('AIAGP5', help_text='AIA_IMG_GP5', blank=True, null=True)
	aiagp6 = models.IntegerField('AIAGP6', help_text='AIA_IMG_GP6', blank=True, null=True)
	aiagp7 = models.IntegerField('AIAGP7', help_text='AIA_IMG_GP7', blank=True, null=True)
	aiagp8 = models.IntegerField('AIAGP8', help_text='AIA_IMG_GP8', blank=True, null=True)
	aiagp9 = models.IntegerField('AIAGP9', help_text='AIA_IMG_GP9', blank=True, null=True)
	aiahfsn = models.IntegerField('AIAHFSN', help_text='AIA_IMG_HIST_FSN', blank=True, null=True)
	aiasen = models.IntegerField('AIASEN', help_text='AIA_IMG_AS_ENCODER', blank=True, null=True)
	aiawvlen = models.IntegerField('AIAWVLEN', help_text='AIA_IMG_WAVELENGTH', blank=True, null=True)
	aicfgdl1 = models.IntegerField('AICFGDL1', help_text='AIA_IMG_CFG_DELAY_1', blank=True, null=True)
	aicfgdl2 = models.IntegerField('AICFGDL2', help_text='AIA_IMG_CFG_DELAY_2', blank=True, null=True)
	aicfgdl3 = models.IntegerField('AICFGDL3', help_text='AIA_IMG_CFG_DELAY_3', blank=True, null=True)
	aicfgdl4 = models.IntegerField('AICFGDL4', help_text='AIA_IMG_CFG_DELAY_4', blank=True, null=True)
	aifcps = models.IntegerField('AIFCPS', help_text='AIA_IMG_FC_POSITION', blank=True, null=True)
	aifdbid = models.IntegerField('AIFDBID', help_text='AIA_IMG_FDB_ID', blank=True, null=True)
	aifiltyp = models.IntegerField('AIFILTYP', help_text='AIA_IMG_FILTER_TYPE', blank=True, null=True)
	aifoenfl = models.IntegerField('AIFOENFL', help_text='AIA_IMG_FOCUS_ENA_FLAG', blank=True, null=True)
	aifrmlid = models.IntegerField('AIFRMLID', help_text='AIA_IMG_FRMLIST_ID', blank=True, null=True)
	aiftsid = models.IntegerField('AIFTSID', help_text='AIA_IMG_FTS_ID', blank=True, null=True)
	aiftswth = models.IntegerField('AIFTSWTH', help_text='AIA_IMG_FLT_TYPE_SW_TH', blank=True, null=True)
	aifwen = models.IntegerField('AIFWEN', help_text='AIA_IMG_FW_ENCODER', blank=True, null=True)
	aihis192 = models.IntegerField('AIHIS192', help_text='AIA_IMG_HISTC_BN_192', blank=True, null=True)
	aihis348 = models.IntegerField('AIHIS348', help_text='AIA_IMG_HISTC_BN_348', blank=True, null=True)
	aihis604 = models.IntegerField('AIHIS604', help_text='AIA_IMG_HISTC_BN_604', blank=True, null=True)
	aihis860 = models.IntegerField('AIHIS860', help_text='AIA_IMG_HISTC_BN_860', blank=True, null=True)
	aihismxb = models.IntegerField('AIHISMXB', help_text='AIA_IMG_HIST_MAX_BIN', blank=True, null=True)
	aimgfsn = models.IntegerField('AIMGFSN', help_text='AIA_IMG_FRLIST_POS', blank=True, null=True)
	aimgots = models.IntegerField('AIMGOTS', help_text='AIA_IMG_OBT_TIME_SH_SEC', blank=True, null=True)
	aimgotss = models.IntegerField('AIMGOTSS', help_text='AIA_IMG_OBT_TIME_SH_SS', blank=True, null=True)
	aimgshce = models.IntegerField('AIMGSHCE', help_text='AIA_IMG_SH_CMDED_EXPOSURE', blank=True, null=True)
	aimgshen = models.IntegerField('AIMGSHEN', help_text='AIA_IMG_SH_ENCODER', blank=True, null=True)
	aimgtyp = models.IntegerField('AIMGTYP', help_text='AIA_IMG_IMAGE_TYPE', blank=True, null=True)
	aimshcbc = models.FloatField('AIMSHCBC', help_text='AIA_IMG_SH_CLOSE_BOT_CENTR', blank=True, null=True)
	aimshcbe = models.FloatField('AIMSHCBE', help_text='AIA_IMG_SH_CLOSE_BOT_EDGE', blank=True, null=True)
	aimshctc = models.FloatField('AIMSHCTC', help_text='AIA_IMG_SH_CLOSE_TOP_CENTR', blank=True, null=True)
	aimshcte = models.FloatField('AIMSHCTE', help_text='AIA_IMG_SH_CLOSE_TOP_EDGE', blank=True, null=True)
	aimshobc = models.FloatField('AIMSHOBC', help_text='AIA_IMG_SH_OPEN_BOT_CENTR', blank=True, null=True)
	aimshobe = models.FloatField('AIMSHOBE', help_text='AIA_IMG_SH_OPEN_BOT_EDGE', blank=True, null=True)
	aimshotc = models.FloatField('AIMSHOTC', help_text='AIA_IMG_SH_OPEN_TOP_CENTR', blank=True, null=True)
	aimshote = models.FloatField('AIMSHOTE', help_text='AIA_IMG_SH_OPEN_TOP_EDGE', blank=True, null=True)
	aistate = models.TextField('AISTATE', help_text='AIA_IMG_ISS_LOOP', blank=True, null=True)
	aivnmst = models.IntegerField('AIVNMST', help_text='AIA_VER_NUM_IMAGE_STATUS', blank=True, null=True)
	asd_rec = models.TextField('ASD_REC', help_text='Ancillary Science Data series record pointer', blank=True, null=True)
	asqfsn = models.IntegerField('ASQFSN', help_text='AIA_SEQ_FRAME_SN', blank=True, null=True)
	asqhdr = models.BigIntegerField('ASQHDR', help_text='AIA_SEQ_HEADER', blank=True, null=True)
	asqtnum = models.IntegerField('ASQTNUM', help_text='AIA_SEQ_TEL_NUM', blank=True, null=True)
	bld_vers = models.TextField('BLD_VERS', help_text='Build Version: from jsoc_version.h', blank=True, null=True)
	camera = models.IntegerField('CAMERA', help_text='For AIA: 1, 2, 3  or 4', blank=True, null=True)
	car_rot = models.IntegerField('CAR_ROT', help_text='Carrington rotation number of CRLN_OBS', blank=True, null=True)
	cdelt1 = models.FloatField('CDELT1', help_text='CDELT1: image scale in the x direction', blank=True, null=True)
	cdelt2 = models.FloatField('CDELT2', help_text='CDELT2: image scale in the y direction', blank=True, null=True)
	crln_obs = models.FloatField('CRLN_OBS', help_text='Carrington longitude of the observer', blank=True, null=True)
	crlt_obs = models.FloatField('CRLT_OBS', help_text='Carrington latitude of the observer', blank=True, null=True)
	crota2 = models.FloatField('CROTA2', help_text='CROTA2: INST_ROT + SAT_ROT', blank=True, null=True)
	crpix1 = models.FloatField('CRPIX1', help_text='CRPIX1: location of sun center in CCD x direction', blank=True, null=True)
	crpix2 = models.FloatField('CRPIX2', help_text='CRPIX2: location of sun center in CCD y direction', blank=True, null=True)
	crval1 = models.FloatField('CRVAL1', help_text='CRVAL1: image scale in the x direction', blank=True, null=True)
	crval2 = models.FloatField('CRVAL2', help_text='CRVAL2: image scale in the x direction', blank=True, null=True)
	ctype1 = models.TextField('CTYPE1', help_text='CTYPE1; Typically HPLN-TAN (SOLARX)', blank=True, null=True)
	ctype2 = models.TextField('CTYPE2', help_text='CTYPE2; Typically HPLT-TAN (SOLARY)', blank=True, null=True)
	cunit1 = models.TextField('CUNIT1', help_text='CUNIT1; Typically arcsec', blank=True, null=True)
	cunit2 = models.TextField('CUNIT2', help_text='CUNIT2; Typically arcsec', blank=True, null=True)
	datacent = models.FloatField('DATACENT', help_text='Median value of center column of the image', blank=True, null=True)
	datakurt = models.FloatField('DATAKURT', help_text='Kurtosis of all pixels', blank=True, null=True)
	datamax = models.IntegerField('DATAMAX', help_text='Maximum value of all pixels', blank=True, null=True)
	datamean = models.FloatField('DATAMEAN', help_text='Mean value of all pixels', blank=True, null=True)
	datamedn = models.IntegerField('DATAMEDN', help_text='Median value of all pixels', blank=True, null=True)
	datamin = models.IntegerField('DATAMIN', help_text='Minimum value of all pixels', blank=True, null=True)
	datap01 = models.FloatField('DATAP01', help_text='DATAP01', blank=True, null=True)
	datap10 = models.FloatField('DATAP10', help_text='DATAP10', blank=True, null=True)
	datap25 = models.FloatField('DATAP25', help_text='DATAP25', blank=True, null=True)
	datap75 = models.FloatField('DATAP75', help_text='DATAP75', blank=True, null=True)
	datap90 = models.FloatField('DATAP90', help_text='DATAP90', blank=True, null=True)
	datap95 = models.FloatField('DATAP95', help_text='DATAP95', blank=True, null=True)
	datap98 = models.FloatField('DATAP98', help_text='DATAP98', blank=True, null=True)
	datap99 = models.FloatField('DATAP99', help_text='DATAP99', blank=True, null=True)
	datarms = models.FloatField('DATARMS', help_text='Rms deviation from the mean value of all pixels', blank=True, null=True)
	dataskew = models.FloatField('DATASKEW', help_text='Skewness from the mean value of all pixels', blank=True, null=True)
	datavals = models.IntegerField('DATAVALS', help_text='Actual number of data values in image', blank=True, null=True)
	date = models.DateTimeField('DATE', help_text='Date_time of processing; ISO 8601', blank=True, null=True)
	date_obs = models.DateTimeField('DATE-OBS', help_text=' Date when observation started; ISO 8601', blank=True, null=True)
	dn_gain = models.FloatField('DN_GAIN', help_text='DN/electron', blank=True, null=True)
	dsun_obs = models.FloatField('DSUN_OBS', help_text='Distance from SDO to Sun center', blank=True, null=True)
	dsun_ref = models.FloatField('DSUN_REF', help_text='Reference distance to Sun: 149,597,870,691.0 m', blank=True, null=True)
	eff_area = models.FloatField('EFF_AREA', help_text='effective area', blank=True, null=True)
	eff_ar_v = models.FloatField('EFF_AR_V', help_text='version # for EFF_AREA and DN_GAIN', blank=True, null=True)
	expsdev = models.FloatField('EXPSDEV', help_text='Exposure standard deviation', blank=True, null=True)
	exptime = models.FloatField('EXPTIME', help_text='Exposure duration: mean shutter open time', blank=True, null=True)
	fid = models.IntegerField('FID', help_text='FID Filtergram ID', blank=True, null=True)
	flat_rec = models.TextField('FLAT_REC', help_text='Flatfield series record pointer', blank=True, null=True)
	fsn = models.IntegerField('FSN', help_text='FSN Filtergram Sequence Number', blank=True, null=True)
	gaex_obs = models.FloatField('GAEX_OBS', help_text='Geocentric Inertial X position', blank=True, null=True)
	gaey_obs = models.FloatField('GAEY_OBS', help_text='Geocentric Inertial Y position', blank=True, null=True)
	gaez_obs = models.FloatField('GAEZ_OBS', help_text='Geocentric Inertial Z position', blank=True, null=True)
	haex_obs = models.FloatField('HAEX_OBS', help_text='Heliocentric Inertial X position', blank=True, null=True)
	haey_obs = models.FloatField('HAEY_OBS', help_text='Heliocentric Inertial Y position', blank=True, null=True)
	haez_obs = models.FloatField('HAEZ_OBS', help_text='Heliocentric Inertial Z position', blank=True, null=True)
	hgln_obs = models.FloatField('HGLN_OBS', help_text='Stonyhurst heliographic longitude of the observer', blank=True, null=True)
	hglt_obs = models.FloatField('HGLT_OBS', help_text='Stonyhurst heliographic latitude of the observer', blank=True, null=True)
	img_type = models.TextField('IMG_TYPE', help_text='Image type: LIGHT or DARK', blank=True, null=True)
	imscl_mp = models.FloatField('IMSCL_MP', help_text='Master pointing image scale', blank=True, null=True)
	inst_rot = models.FloatField('INST_ROT', help_text='Master pointing CCD rotation wrt SDO Z axis', blank=True, null=True)
	instrume = models.TextField('INSTRUME', help_text='For AIA: AIA_ATA1, AIA_ATA2, AIA_ATA3 or AIA_ATA4', blank=True, null=True)
	int_time = models.FloatField('INT_TIME', help_text='CCD integration duration', blank=True, null=True)
	isppktim = models.DateTimeField('ISPPKTIM', help_text='PACKET_TIME, Prime key value for the ISP record', blank=True, null=True)
	isppktvn = models.TextField('ISPPKTVN', help_text='PACKET_VERSION_NUMBER', blank=True, null=True)
	ispsname = models.TextField('ISPSNAME', help_text='ISP SERIES NAME', blank=True, null=True)
	keywddoc = models.TextField('KEYWDDOC', help_text='AIA FITS keyword documentation', blank=True, null=True)
	lvl_num = models.FloatField('LVL_NUM', help_text='LVL_NUM data level number', blank=True, null=True)
	missvals = models.IntegerField('MISSVALS', help_text='Missing values: TOTVALS - DATAVALS', blank=True, null=True)
	mpo_rec = models.TextField('MPO_REC', help_text='Master Pointing series record pointer', blank=True, null=True)
	nsatpix = models.IntegerField('NSATPIX', help_text='Number of saturated pixels detected in image', blank=True, null=True)
	nspikes = models.IntegerField('NSPIKES', help_text='Number of cosmic ray affected pixels detected in image', blank=True, null=True)
	obs_vn = models.FloatField('OBS_VN', help_text='Speed of observer in solar-north direction', blank=True, null=True)
	obs_vr = models.FloatField('OBS_VR', help_text='Speed of observer in radial direction', blank=True, null=True)
	obs_vw = models.FloatField('OBS_VW', help_text='Speed of observer in solar-west direction', blank=True, null=True)
	orb_rec = models.TextField('ORB_REC', help_text='Orbit vector series record pointer', blank=True, null=True)
	origin = models.TextField('ORIGIN', help_text='ORIGIN Location where file made', blank=True, null=True)
	oscnmean = models.FloatField('OSCNMEAN', help_text='Mean value of oversan rows', blank=True, null=True)
	oscnrms = models.FloatField('OSCNRMS', help_text='Rms deviation from the mean value of overscan rows', blank=True, null=True)
	percentd = models.FloatField('PERCENTD', help_text='Percent data; 100*DATAVALS/TOTVALS', blank=True, null=True)
	pixlunit = models.TextField('PIXLUNIT', help_text='Pixel intensity unit', blank=True, null=True)
	quality = models.IntegerField('QUALITY', help_text='Level 1 Quality word', blank=True, null=True)
	quallev0 = models.IntegerField('QUALLEV0', help_text='Level 0 Quality word', blank=True, null=True)
	recnum = models.BigIntegerField('RECNUM', help_text='JSOC Record Number', blank=True, null=True)
	roi_llx1 = models.IntegerField('ROI_LLX1', help_text='CCD X location of lower left corner of ROI1', blank=True, null=True)
	roi_llx2 = models.IntegerField('ROI_LLX2', help_text='CCD X location of lower left corner of ROI2', blank=True, null=True)
	roi_lly1 = models.IntegerField('ROI_LLY1', help_text='CCD Y location of lower left corner of ROI1', blank=True, null=True)
	roi_lly2 = models.IntegerField('ROI_LLY2', help_text='CCD Y location of lower left corner of ROI2', blank=True, null=True)
	roi_nax1 = models.IntegerField('ROI_NAX1', help_text='Number of CCD columns for width of ROI1', blank=True, null=True)
	roi_nax2 = models.IntegerField('ROI_NAX2', help_text='Number of CCD columns for width of ROI2', blank=True, null=True)
	roi_nay1 = models.IntegerField('ROI_NAY1', help_text='Number of CCD rows for height of ROI1', blank=True, null=True)
	roi_nay2 = models.IntegerField('ROI_NAY2', help_text='Number of CCD rows for height of ROI2', blank=True, null=True)
	roi_nwin = models.IntegerField('ROI_NWIN', help_text='Number of Windows for Region of Interest (ROI)', blank=True, null=True)
	roi_sum = models.IntegerField('ROI_SUM', help_text='Summing Mode: 1x1, 2x2, 4x4 (0,1,2)', blank=True, null=True)
	r_sun = models.FloatField('R_SUN', help_text='Radius of the Sun in pixels on the CCD detector', blank=True, null=True)
	rsun_obs = models.FloatField('RSUN_OBS', help_text='Apparent radius of the Sun seen by SDO', blank=True, null=True)
	rsun_ref = models.FloatField('RSUN_REF', help_text='Reference radius of the Sun: 696,000,000.0 m', blank=True, null=True)
	sat_rot = models.FloatField('SAT_ROT', help_text='Angle of solar pole wrt the SDO X axis', blank=True, null=True)
	sat_y0 = models.FloatField('SAT_Y0', help_text='Position of solar center wrt the SDO -Y axis', blank=True, null=True)
	sat_z0 = models.FloatField('SAT_Z0', help_text='Position of solar center wrt the SDO Z axis', blank=True, null=True)
	segment = models.TextField('SEGMENT', help_text='JSOC Segment File Name', blank=True, null=True)
	series = models.TextField('SERIES', help_text='JSOC Series Name', blank=True, null=True)
	slotnum = models.IntegerField('SLOTNUM', help_text='JSOC Slot Number', blank=True, null=True)
	sunum = models.BigIntegerField('SUNUM', help_text='JSOC Storage Unit Number', blank=True, null=True)
	telescop = models.TextField('TELESCOP', help_text='For AIA: SDO/AIA', blank=True, null=True)
	tempccd = models.FloatField('TEMPCCD', help_text='CCD temperature: CCD_HEADER1', blank=True, null=True)
	tempfpad = models.FloatField('TEMPFPAD', help_text='Focal plane assembly adapter temperature: FPA_ADAPTER', blank=True, null=True)
	tempgt = models.FloatField('TEMPGT', help_text='Guide telescope temperature: GT_1', blank=True, null=True)
	tempsmir = models.FloatField('TEMPSMIR', help_text='Secondary mirror temperature : SEC_MIRROR', blank=True, null=True)
	t_obs = models.DateTimeField('T_OBS', help_text='Observation time', blank=True, null=True)
	totvals = models.IntegerField('TOTVALS', help_text='Expected number of data values (pixels)', blank=True, null=True)
	t_rec = models.DateTimeField('T_REC', help_text='Slotted observation time', blank=True, null=True)
	wavelnth = models.IntegerField('WAVELNTH', help_text='Wavelength', blank=True, null=True)
	wave_str = models.TextField('WAVE_STR', help_text='Wavelength_FilterPosition', blank=True, null=True)
	waveunit = models.TextField('WAVEUNIT', help_text='Wavelength unit: angstrom', blank=True, null=True)
	x0_mp = models.FloatField('X0_MP', help_text='Master pointing X0 sun center in CCD frame', blank=True, null=True)
	y0_mp = models.FloatField('Y0_MP', help_text='Master pointing Y0 sun center in CCD frame', blank=True, null=True)
