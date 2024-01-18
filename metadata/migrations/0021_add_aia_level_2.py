# Generated by Django 3.2.13 on 2024-01-18 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
        ('metadata', '0020_remove_model_field_fits_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='AiaLevel2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.TextField(db_index=True, help_text='Unique identification string for the observation metadata, usually in the form YYYYMMDDHHMMSS; cannot be modified once it is set', unique=True, verbose_name='Observation ID')),
                ('date_beg', models.DateTimeField(blank=True, db_index=True, help_text='Start time of the observation [UTC]', null=True, verbose_name='DATE-BEG')),
                ('date_end', models.DateTimeField(blank=True, db_index=True, help_text='End time of the observation [UTC]', null=True, verbose_name='DATE-END')),
                ('wavemin', models.FloatField(blank=True, db_index=True, help_text='Min value of the observation spectral range [nm]', null=True, verbose_name='WAVEMIN')),
                ('wavemax', models.FloatField(blank=True, db_index=True, help_text='Max value of the observation spectral range [nm]', null=True, verbose_name='WAVEMAX')),
                ('acs_cgt', models.TextField(blank=True, help_text='ACS ID of Controlling Guide Telescope - ACS_AN_NUM_CGT', null=True, verbose_name='ACS_CGT')),
                ('acs_eclp', models.TextField(blank=True, help_text='ACS eclipse flag - ACS_AN_FLAG_CSS_ECLIPSE', null=True, verbose_name='ACS_ECLP')),
                ('acs_mode', models.TextField(blank=True, help_text='ACS pointing mode - ACS_AN_ACS_MODE', null=True, verbose_name='ACS_MODE')),
                ('acs_safe', models.TextField(blank=True, help_text='ACS safe hold flag - ACS_AN_FLAG_ACE_INSAFEHOLD', null=True, verbose_name='ACS_SAFE')),
                ('acs_sunp', models.TextField(blank=True, help_text='ACS sun presense flag - ACS_AN_FLAG_DSS_SUNPRES', null=True, verbose_name='ACS_SUNP')),
                ('aecdelay', models.BigIntegerField(blank=True, help_text='AIA_IMG_AEC_DELAY', null=True, verbose_name='AECDELAY')),
                ('aecmode', models.TextField(blank=True, help_text='AIA_IMG_AEC_MODE', null=True, verbose_name='AECMODE')),
                ('aectype', models.BigIntegerField(blank=True, help_text='AIA_IMG_AEC_TYPE', null=True, verbose_name='AECTYPE')),
                ('agt1svy', models.BigIntegerField(blank=True, help_text='AIA_GT1_SUNVECTOR_Y', null=True, verbose_name='AGT1SVY')),
                ('agt1svz', models.BigIntegerField(blank=True, help_text='AIA_GT1_SUNVECTOR_Z', null=True, verbose_name='AGT1SVZ')),
                ('agt2svy', models.BigIntegerField(blank=True, help_text='AIA_GT2_SUNVECTOR_Y', null=True, verbose_name='AGT2SVY')),
                ('agt2svz', models.BigIntegerField(blank=True, help_text='AIA_GT2_SUNVECTOR_Z', null=True, verbose_name='AGT2SVZ')),
                ('agt3svy', models.BigIntegerField(blank=True, help_text='AIA_GT3_SUNVECTOR_Y', null=True, verbose_name='AGT3SVY')),
                ('agt3svz', models.BigIntegerField(blank=True, help_text='AIA_GT3_SUNVECTOR_Z', null=True, verbose_name='AGT3SVZ')),
                ('agt4svy', models.BigIntegerField(blank=True, help_text='AIA_GT4_SUNVECTOR_Y', null=True, verbose_name='AGT4SVY')),
                ('agt4svz', models.BigIntegerField(blank=True, help_text='AIA_GT4_SUNVECTOR_Z', null=True, verbose_name='AGT4SVZ')),
                ('aiaecenf', models.BigIntegerField(blank=True, help_text='AIA_IMG_AEC_ENA_FLAG', null=True, verbose_name='AIAECENF')),
                ('aiaecti', models.BigIntegerField(blank=True, help_text='AIA_IMG_AEC_TABLE_ID', null=True, verbose_name='AIAECTI')),
                ('aiagp1', models.BigIntegerField(blank=True, help_text='AIA_IMG_GP1', null=True, verbose_name='AIAGP1')),
                ('aiagp10', models.BigIntegerField(blank=True, help_text='AIA_IMG_GP10', null=True, verbose_name='AIAGP10')),
                ('aiagp2', models.BigIntegerField(blank=True, help_text='AIA_IMG_GP2', null=True, verbose_name='AIAGP2')),
                ('aiagp3', models.BigIntegerField(blank=True, help_text='AIA_IMG_GP3', null=True, verbose_name='AIAGP3')),
                ('aiagp4', models.BigIntegerField(blank=True, help_text='AIA_IMG_GP4', null=True, verbose_name='AIAGP4')),
                ('aiagp5', models.BigIntegerField(blank=True, help_text='AIA_IMG_GP5', null=True, verbose_name='AIAGP5')),
                ('aiagp6', models.BigIntegerField(blank=True, help_text='AIA_IMG_GP6', null=True, verbose_name='AIAGP6')),
                ('aiagp7', models.BigIntegerField(blank=True, help_text='AIA_IMG_GP7', null=True, verbose_name='AIAGP7')),
                ('aiagp8', models.BigIntegerField(blank=True, help_text='AIA_IMG_GP8', null=True, verbose_name='AIAGP8')),
                ('aiagp9', models.BigIntegerField(blank=True, help_text='AIA_IMG_GP9', null=True, verbose_name='AIAGP9')),
                ('aiahfsn', models.BigIntegerField(blank=True, help_text='AIA_IMG_HIST_FSN', null=True, verbose_name='AIAHFSN')),
                ('aiasen', models.BigIntegerField(blank=True, help_text='AIA_IMG_AS_ENCODER', null=True, verbose_name='AIASEN')),
                ('aiawvlen', models.BigIntegerField(blank=True, help_text='AIA_IMG_WAVELENGTH', null=True, verbose_name='AIAWVLEN')),
                ('aicfgdl1', models.BigIntegerField(blank=True, help_text='AIA_IMG_CFG_DELAY_1', null=True, verbose_name='AICFGDL1')),
                ('aicfgdl2', models.BigIntegerField(blank=True, help_text='AIA_IMG_CFG_DELAY_2', null=True, verbose_name='AICFGDL2')),
                ('aicfgdl3', models.BigIntegerField(blank=True, help_text='AIA_IMG_CFG_DELAY_3', null=True, verbose_name='AICFGDL3')),
                ('aicfgdl4', models.BigIntegerField(blank=True, help_text='AIA_IMG_CFG_DELAY_4', null=True, verbose_name='AICFGDL4')),
                ('aifcps', models.BigIntegerField(blank=True, help_text='AIA_IMG_FC_POSITION', null=True, verbose_name='AIFCPS')),
                ('aifdbid', models.BigIntegerField(blank=True, help_text='AIA_IMG_FDB_ID', null=True, verbose_name='AIFDBID')),
                ('aifiltyp', models.BigIntegerField(blank=True, help_text='AIA_IMG_FILTER_TYPE', null=True, verbose_name='AIFILTYP')),
                ('aifoenfl', models.BigIntegerField(blank=True, help_text='AIA_IMG_FOCUS_ENA_FLAG', null=True, verbose_name='AIFOENFL')),
                ('aifrmlid', models.BigIntegerField(blank=True, help_text='AIA_IMG_FRMLIST_ID', null=True, verbose_name='AIFRMLID')),
                ('aiftsid', models.BigIntegerField(blank=True, help_text='AIA_IMG_FTS_ID', null=True, verbose_name='AIFTSID')),
                ('aiftswth', models.BigIntegerField(blank=True, help_text='AIA_IMG_FLT_TYPE_SW_TH', null=True, verbose_name='AIFTSWTH')),
                ('aifwen', models.BigIntegerField(blank=True, help_text='AIA_IMG_FW_ENCODER', null=True, verbose_name='AIFWEN')),
                ('aihis192', models.BigIntegerField(blank=True, help_text='AIA_IMG_HISTC_BN_192', null=True, verbose_name='AIHIS192')),
                ('aihis348', models.BigIntegerField(blank=True, help_text='AIA_IMG_HISTC_BN_348', null=True, verbose_name='AIHIS348')),
                ('aihis604', models.BigIntegerField(blank=True, help_text='AIA_IMG_HISTC_BN_604', null=True, verbose_name='AIHIS604')),
                ('aihis860', models.BigIntegerField(blank=True, help_text='AIA_IMG_HISTC_BN_860', null=True, verbose_name='AIHIS860')),
                ('aihismxb', models.BigIntegerField(blank=True, help_text='AIA_IMG_HIST_MAX_BIN', null=True, verbose_name='AIHISMXB')),
                ('aimgfsn', models.BigIntegerField(blank=True, help_text='AIA_IMG_FRLIST_POS', null=True, verbose_name='AIMGFSN')),
                ('aimgots', models.BigIntegerField(blank=True, help_text='AIA_IMG_OBT_TIME_SH_SEC', null=True, verbose_name='AIMGOTS')),
                ('aimgotss', models.BigIntegerField(blank=True, help_text='AIA_IMG_OBT_TIME_SH_SS', null=True, verbose_name='AIMGOTSS')),
                ('aimgshce', models.BigIntegerField(blank=True, help_text='AIA_IMG_SH_CMDED_EXPOSURE', null=True, verbose_name='AIMGSHCE')),
                ('aimgshen', models.BigIntegerField(blank=True, help_text='AIA_IMG_SH_ENCODER', null=True, verbose_name='AIMGSHEN')),
                ('aimgtyp', models.BigIntegerField(blank=True, help_text='AIA_IMG_IMAGE_TYPE', null=True, verbose_name='AIMGTYP')),
                ('aimshcbc', models.FloatField(blank=True, help_text='AIA_IMG_SH_CLOSE_BOT_CENTR', null=True, verbose_name='AIMSHCBC')),
                ('aimshcbe', models.FloatField(blank=True, help_text='AIA_IMG_SH_CLOSE_BOT_EDGE', null=True, verbose_name='AIMSHCBE')),
                ('aimshctc', models.FloatField(blank=True, help_text='AIA_IMG_SH_CLOSE_TOP_CENTR', null=True, verbose_name='AIMSHCTC')),
                ('aimshcte', models.FloatField(blank=True, help_text='AIA_IMG_SH_CLOSE_TOP_EDGE', null=True, verbose_name='AIMSHCTE')),
                ('aimshobc', models.FloatField(blank=True, help_text='AIA_IMG_SH_OPEN_BOT_CENTR', null=True, verbose_name='AIMSHOBC')),
                ('aimshobe', models.FloatField(blank=True, help_text='AIA_IMG_SH_OPEN_BOT_EDGE', null=True, verbose_name='AIMSHOBE')),
                ('aimshotc', models.FloatField(blank=True, help_text='AIA_IMG_SH_OPEN_TOP_CENTR', null=True, verbose_name='AIMSHOTC')),
                ('aimshote', models.FloatField(blank=True, help_text='AIA_IMG_SH_OPEN_TOP_EDGE', null=True, verbose_name='AIMSHOTE')),
                ('aistate', models.TextField(blank=True, help_text='AIA_IMG_ISS_LOOP', null=True, verbose_name='AISTATE')),
                ('aivnmst', models.BigIntegerField(blank=True, help_text='AIA_VER_NUM_IMAGE_STATUS', null=True, verbose_name='AIVNMST')),
                ('asd_rec', models.TextField(blank=True, help_text='Ancillary Science Data series record pointer', null=True, verbose_name='ASD_REC')),
                ('asqfsn', models.BigIntegerField(blank=True, help_text='AIA_SEQ_FRAME_SN', null=True, verbose_name='ASQFSN')),
                ('asqhdr', models.BigIntegerField(blank=True, help_text='AIA_SEQ_HEADER', null=True, verbose_name='ASQHDR')),
                ('asqtnum', models.BigIntegerField(blank=True, help_text='AIA_SEQ_TEL_NUM', null=True, verbose_name='ASQTNUM')),
                ('bld_vers', models.TextField(blank=True, help_text='Build Version: from jsoc_version.h', null=True, verbose_name='BLD_VERS')),
                ('calver32', models.BigIntegerField(blank=True, help_text='Calibration Version {ROI_NWIN}', null=True, verbose_name='CALVER32')),
                ('camera', models.BigIntegerField(blank=True, help_text='For AIA: 1, 2, 3  or 4', null=True, verbose_name='CAMERA')),
                ('car_rot', models.BigIntegerField(blank=True, help_text='Carrington rotation number of CRLN_OBS', null=True, verbose_name='CAR_ROT')),
                ('cdelt1', models.FloatField(blank=True, help_text='CDELT1: image scale in the x direction', null=True, verbose_name='CDELT1')),
                ('cdelt2', models.FloatField(blank=True, help_text='CDELT2: image scale in the y direction', null=True, verbose_name='CDELT2')),
                ('crln_obs', models.FloatField(blank=True, help_text='Carrington longitude of the observer', null=True, verbose_name='CRLN_OBS')),
                ('crlt_obs', models.FloatField(blank=True, help_text='Carrington latitude of the observer', null=True, verbose_name='CRLT_OBS')),
                ('crota2', models.FloatField(blank=True, help_text='CROTA2: INST_ROT + SAT_ROT', null=True, verbose_name='CROTA2')),
                ('crpix1', models.FloatField(blank=True, help_text='CRPIX1: location of sun center in CCD x direction', null=True, verbose_name='CRPIX1')),
                ('crpix2', models.FloatField(blank=True, help_text='CRPIX2: location of sun center in CCD y direction', null=True, verbose_name='CRPIX2')),
                ('crval1', models.FloatField(blank=True, help_text='CRVAL1: image scale in the x direction', null=True, verbose_name='CRVAL1')),
                ('crval2', models.FloatField(blank=True, help_text='CRVAL2: image scale in the x direction', null=True, verbose_name='CRVAL2')),
                ('ctype1', models.TextField(blank=True, help_text='CTYPE1; Typically HPLN-TAN (SOLARX)', null=True, verbose_name='CTYPE1')),
                ('ctype2', models.TextField(blank=True, help_text='CTYPE2; Typically HPLT-TAN (SOLARY)', null=True, verbose_name='CTYPE2')),
                ('cunit1', models.TextField(blank=True, help_text='CUNIT1; Typically arcsec', null=True, verbose_name='CUNIT1')),
                ('cunit2', models.TextField(blank=True, help_text='CUNIT2; Typically arcsec', null=True, verbose_name='CUNIT2')),
                ('datacent', models.FloatField(blank=True, help_text='Median value of center column of the image', null=True, verbose_name='DATACENT')),
                ('datakurt', models.FloatField(blank=True, help_text='Kurtosis of all pixels', null=True, verbose_name='DATAKURT')),
                ('datamax', models.BigIntegerField(blank=True, help_text='Maximum value of all pixels', null=True, verbose_name='DATAMAX')),
                ('datamean', models.FloatField(blank=True, help_text='Mean value of all pixels', null=True, verbose_name='DATAMEAN')),
                ('datamedn', models.BigIntegerField(blank=True, help_text='Median value of all pixels', null=True, verbose_name='DATAMEDN')),
                ('datamin', models.BigIntegerField(blank=True, help_text='Minimum value of all pixels', null=True, verbose_name='DATAMIN')),
                ('datap01', models.FloatField(blank=True, help_text='DATAP01', null=True, verbose_name='DATAP01')),
                ('datap10', models.FloatField(blank=True, help_text='DATAP10', null=True, verbose_name='DATAP10')),
                ('datap25', models.FloatField(blank=True, help_text='DATAP25', null=True, verbose_name='DATAP25')),
                ('datap75', models.FloatField(blank=True, help_text='DATAP75', null=True, verbose_name='DATAP75')),
                ('datap90', models.FloatField(blank=True, help_text='DATAP90', null=True, verbose_name='DATAP90')),
                ('datap95', models.FloatField(blank=True, help_text='DATAP95', null=True, verbose_name='DATAP95')),
                ('datap98', models.FloatField(blank=True, help_text='DATAP98', null=True, verbose_name='DATAP98')),
                ('datap99', models.FloatField(blank=True, help_text='DATAP99', null=True, verbose_name='DATAP99')),
                ('datarms', models.FloatField(blank=True, help_text='Rms deviation from the mean value of all pixels', null=True, verbose_name='DATARMS')),
                ('dataskew', models.FloatField(blank=True, help_text='Skewness from the mean value of all pixels', null=True, verbose_name='DATASKEW')),
                ('datavals', models.BigIntegerField(blank=True, help_text='Actual number of data values in image', null=True, verbose_name='DATAVALS')),
                ('date', models.DateTimeField(blank=True, help_text='Date_time of processing; ISO 8601', null=True, verbose_name='DATE')),
                ('date_obs', models.DateTimeField(blank=True, help_text=' Date when observation started; ISO 8601', null=True, verbose_name='DATE-OBS')),
                ('dn_gain', models.FloatField(blank=True, help_text='DN/electron', null=True, verbose_name='DN_GAIN')),
                ('drms_id', models.TextField(blank=True, help_text='DRMS ID', null=True, verbose_name='DRMS_ID')),
                ('dsun_obs', models.FloatField(blank=True, help_text='Distance from SDO to Sun center', null=True, verbose_name='DSUN_OBS')),
                ('dsun_ref', models.FloatField(blank=True, help_text='Reference distance to Sun: 149,597,870,691.0 m', null=True, verbose_name='DSUN_REF')),
                ('eff_ar_v', models.FloatField(blank=True, help_text='version # for EFF_AREA and DN_GAIN', null=True, verbose_name='EFF_AR_V')),
                ('eff_area', models.FloatField(blank=True, help_text='effective area', null=True, verbose_name='EFF_AREA')),
                ('expsdev', models.FloatField(blank=True, help_text='Exposure standard deviation', null=True, verbose_name='EXPSDEV')),
                ('exptime', models.FloatField(blank=True, help_text='Exposure duration: mean shutter open time', null=True, verbose_name='EXPTIME')),
                ('fid', models.BigIntegerField(blank=True, help_text='FID Filtergram ID', null=True, verbose_name='FID')),
                ('flat_rec', models.TextField(blank=True, help_text='Flatfield series record pointer', null=True, verbose_name='FLAT_REC')),
                ('fsn', models.BigIntegerField(blank=True, help_text='FSN Filtergram Sequence Number', null=True, verbose_name='FSN')),
                ('gaex_obs', models.FloatField(blank=True, help_text='Geocentric Inertial X position', null=True, verbose_name='GAEX_OBS')),
                ('gaey_obs', models.FloatField(blank=True, help_text='Geocentric Inertial Y position', null=True, verbose_name='GAEY_OBS')),
                ('gaez_obs', models.FloatField(blank=True, help_text='Geocentric Inertial Z position', null=True, verbose_name='GAEZ_OBS')),
                ('haex_obs', models.FloatField(blank=True, help_text='Heliocentric Inertial X position', null=True, verbose_name='HAEX_OBS')),
                ('haey_obs', models.FloatField(blank=True, help_text='Heliocentric Inertial Y position', null=True, verbose_name='HAEY_OBS')),
                ('haez_obs', models.FloatField(blank=True, help_text='Heliocentric Inertial Z position', null=True, verbose_name='HAEZ_OBS')),
                ('hgln_obs', models.FloatField(blank=True, help_text='Stonyhurst heliographic longitude of the observer', null=True, verbose_name='HGLN_OBS')),
                ('hglt_obs', models.FloatField(blank=True, help_text='Stonyhurst heliographic latitude of the observer', null=True, verbose_name='HGLT_OBS')),
                ('img_type', models.TextField(blank=True, help_text='Image type: LIGHT or DARK', null=True, verbose_name='IMG_TYPE')),
                ('imscl_mp', models.FloatField(blank=True, help_text='Master pointing image scale', null=True, verbose_name='IMSCL_MP')),
                ('inst_rot', models.FloatField(blank=True, help_text='Master pointing CCD rotation wrt SDO Z axis', null=True, verbose_name='INST_ROT')),
                ('instrume', models.TextField(blank=True, help_text='For AIA: AIA_ATA1, AIA_ATA2, AIA_ATA3 or AIA_ATA4', null=True, verbose_name='INSTRUME')),
                ('int_time', models.FloatField(blank=True, help_text='CCD integration duration', null=True, verbose_name='INT_TIME')),
                ('isppktim', models.DateTimeField(blank=True, help_text='PACKET_TIME, Prime key value for the ISP record', null=True, verbose_name='ISPPKTIM')),
                ('isppktvn', models.TextField(blank=True, help_text='PACKET_VERSION_NUMBER', null=True, verbose_name='ISPPKTVN')),
                ('ispsname', models.TextField(blank=True, help_text='ISP SERIES NAME', null=True, verbose_name='ISPSNAME')),
                ('keywddoc', models.TextField(blank=True, help_text='AIA FITS keyword documentation', null=True, verbose_name='KEYWDDOC')),
                ('lvl_num', models.FloatField(blank=True, help_text='LVL_NUM data level number', null=True, verbose_name='LVL_NUM')),
                ('missvals', models.BigIntegerField(blank=True, help_text='Missing values: TOTVALS - DATAVALS', null=True, verbose_name='MISSVALS')),
                ('mpo_rec', models.TextField(blank=True, help_text='Master Pointing series record pointer', null=True, verbose_name='MPO_REC')),
                ('nsatpix', models.BigIntegerField(blank=True, help_text='Number of saturated pixels detected in image', null=True, verbose_name='NSATPIX')),
                ('nspikes', models.BigIntegerField(blank=True, help_text='Number of cosmic ray affected pixels detected in image', null=True, verbose_name='NSPIKES')),
                ('obs_vn', models.FloatField(blank=True, help_text='Speed of observer in solar-north direction', null=True, verbose_name='OBS_VN')),
                ('obs_vr', models.FloatField(blank=True, help_text='Speed of observer in radial direction', null=True, verbose_name='OBS_VR')),
                ('obs_vw', models.FloatField(blank=True, help_text='Speed of observer in solar-west direction', null=True, verbose_name='OBS_VW')),
                ('orb_rec', models.TextField(blank=True, help_text='Orbit vector series record pointer', null=True, verbose_name='ORB_REC')),
                ('origin', models.TextField(blank=True, help_text='ORIGIN Location where file made', null=True, verbose_name='ORIGIN')),
                ('oscnmean', models.FloatField(blank=True, help_text='Mean value of oversan rows', null=True, verbose_name='OSCNMEAN')),
                ('oscnrms', models.FloatField(blank=True, help_text='Rms deviation from the mean value of overscan rows', null=True, verbose_name='OSCNRMS')),
                ('pc1_1', models.FloatField(blank=True, null=True, verbose_name='PC1_1')),
                ('pc1_2', models.FloatField(blank=True, null=True, verbose_name='PC1_2')),
                ('pc2_1', models.FloatField(blank=True, null=True, verbose_name='PC2_1')),
                ('pc2_2', models.FloatField(blank=True, null=True, verbose_name='PC2_2')),
                ('percentd', models.FloatField(blank=True, help_text='Percent data; 100*DATAVALS/TOTVALS', null=True, verbose_name='PERCENTD')),
                ('pixlunit', models.TextField(blank=True, help_text='Pixel intensity unit', null=True, verbose_name='PIXLUNIT')),
                ('quality', models.BigIntegerField(blank=True, help_text='Level 1 Quality word', null=True, verbose_name='QUALITY')),
                ('quallev0', models.BigIntegerField(blank=True, help_text='Level 0 Quality word', null=True, verbose_name='QUALLEV0')),
                ('r_sun', models.FloatField(blank=True, help_text='Radius of the Sun in pixels on the CCD detector', null=True, verbose_name='R_SUN')),
                ('recnum', models.BigIntegerField(blank=True, help_text='JSOC Record Number', null=True, verbose_name='RECNUM')),
                ('roi_llx1', models.BigIntegerField(blank=True, help_text='CCD X location of lower left corner of ROI1', null=True, verbose_name='ROI_LLX1')),
                ('roi_llx2', models.BigIntegerField(blank=True, help_text='CCD X location of lower left corner of ROI2', null=True, verbose_name='ROI_LLX2')),
                ('roi_lly1', models.BigIntegerField(blank=True, help_text='CCD Y location of lower left corner of ROI1', null=True, verbose_name='ROI_LLY1')),
                ('roi_lly2', models.BigIntegerField(blank=True, help_text='CCD Y location of lower left corner of ROI2', null=True, verbose_name='ROI_LLY2')),
                ('roi_nax1', models.BigIntegerField(blank=True, help_text='Number of CCD columns for width of ROI1', null=True, verbose_name='ROI_NAX1')),
                ('roi_nax2', models.BigIntegerField(blank=True, help_text='Number of CCD columns for width of ROI2', null=True, verbose_name='ROI_NAX2')),
                ('roi_nay1', models.BigIntegerField(blank=True, help_text='Number of CCD rows for height of ROI1', null=True, verbose_name='ROI_NAY1')),
                ('roi_nay2', models.BigIntegerField(blank=True, help_text='Number of CCD rows for height of ROI2', null=True, verbose_name='ROI_NAY2')),
                ('roi_nwin', models.BigIntegerField(blank=True, help_text='Number of Windows for Region of Interest (ROI)', null=True, verbose_name='ROI_NWIN')),
                ('roi_sum', models.BigIntegerField(blank=True, help_text='Summing Mode: 1x1, 2x2, 4x4 (0,1,2)', null=True, verbose_name='ROI_SUM')),
                ('rsun_obs', models.FloatField(blank=True, help_text='Apparent radius of the Sun seen by SDO', null=True, verbose_name='RSUN_OBS')),
                ('rsun_ref', models.FloatField(blank=True, help_text='Reference radius of the Sun: 696,000,000.0 m', null=True, verbose_name='RSUN_REF')),
                ('sat_rot', models.FloatField(blank=True, help_text='Angle of solar pole wrt the SDO X axis', null=True, verbose_name='SAT_ROT')),
                ('sat_y0', models.FloatField(blank=True, help_text='Position of solar center wrt the SDO -Y axis', null=True, verbose_name='SAT_Y0')),
                ('sat_z0', models.FloatField(blank=True, help_text='Position of solar center wrt the SDO Z axis', null=True, verbose_name='SAT_Z0')),
                ('segment', models.TextField(blank=True, help_text='JSOC Segment File Name', null=True, verbose_name='SEGMENT')),
                ('series', models.TextField(blank=True, help_text='JSOC Series Name', null=True, verbose_name='SERIES')),
                ('slotnum', models.BigIntegerField(blank=True, help_text='JSOC Slot Number', null=True, verbose_name='SLOTNUM')),
                ('sunum', models.BigIntegerField(blank=True, help_text='JSOC Storage Unit Number', null=True, verbose_name='SUNUM')),
                ('t_obs', models.DateTimeField(blank=True, help_text='Observation time', null=True, verbose_name='T_OBS')),
                ('t_rec', models.DateTimeField(blank=True, help_text='Slotted observation time', null=True, verbose_name='T_REC')),
                ('telescop', models.TextField(blank=True, help_text='For AIA: SDO/AIA', null=True, verbose_name='TELESCOP')),
                ('tempccd', models.FloatField(blank=True, help_text='CCD temperature: CCD_HEADER1', null=True, verbose_name='TEMPCCD')),
                ('tempfpad', models.FloatField(blank=True, help_text='Focal plane assembly adapter temperature: FPA_ADAPTER', null=True, verbose_name='TEMPFPAD')),
                ('tempgt', models.FloatField(blank=True, help_text='Guide telescope temperature: GT_1', null=True, verbose_name='TEMPGT')),
                ('tempsmir', models.FloatField(blank=True, help_text='Secondary mirror temperature : SEC_MIRROR', null=True, verbose_name='TEMPSMIR')),
                ('totvals', models.BigIntegerField(blank=True, help_text='Expected number of data values (pixels)', null=True, verbose_name='TOTVALS')),
                ('wave_str', models.TextField(blank=True, help_text='Wavelength_FilterPosition', null=True, verbose_name='WAVE_STR')),
                ('wavelnth', models.BigIntegerField(blank=True, help_text='Wavelength', null=True, verbose_name='WAVELNTH')),
                ('waveunit', models.TextField(blank=True, help_text='Wavelength unit: angstrom', null=True, verbose_name='WAVEUNIT')),
                ('x0_mp', models.FloatField(blank=True, help_text='Master pointing X0 sun center in CCD frame', null=True, verbose_name='X0_MP')),
                ('y0_mp', models.FloatField(blank=True, help_text='Master pointing Y0 sun center in CCD frame', null=True, verbose_name='Y0_MP')),
                ('data_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadata_aialevel2', to='dataset.datalocation')),
                ('tags', models.ManyToManyField(blank=True, related_name='metadata_aialevel2', to='metadata.Tag')),
            ],
            options={
                'verbose_name': 'AIA level 2 metadata',
                'verbose_name_plural': 'AIA level 2 metadata',
                'ordering': ['date_beg'],
                'abstract': False,
            },
        ),
    ]
