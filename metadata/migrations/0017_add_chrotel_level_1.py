# Generated by Django 3.2.13 on 2023-05-05 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
        ('metadata', '0016_remove_themis'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChrotelLevel1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.TextField(db_index=True, help_text='Unique identification string for the observation metadata, usually in the form YYYYMMDDHHMMSS; cannot be modified once it is set', unique=True, verbose_name='Observation ID')),
                ('fits_header', models.TextField(blank=True, null=True)),
                ('date_beg', models.DateTimeField(blank=True, db_index=True, help_text='Start time of the observation [UTC]', null=True, verbose_name='DATE-BEG')),
                ('date_end', models.DateTimeField(blank=True, db_index=True, help_text='End time of the observation [UTC]', null=True, verbose_name='DATE-END')),
                ('wavemin', models.FloatField(blank=True, db_index=True, help_text='Min value of the observation spectral range [nm]', null=True, verbose_name='WAVEMIN')),
                ('wavemax', models.FloatField(blank=True, db_index=True, help_text='Max value of the observation spectral range [nm]', null=True, verbose_name='WAVEMAX')),
                ('access_estsize', models.BigIntegerField(blank=True, help_text='Estimated file size in kbyte.', null=True, verbose_name='access_estsize')),
                ('access_format', models.TextField(blank=True, help_text='File format type (RFC 6838 Media Type a.k.a. MIME type)', null=True, verbose_name='access_format')),
                ('access_url', models.TextField(blank=True, help_text='URL of the data file, case sensitive. If present, then access_format and access_estsize are mandatory.', null=True, verbose_name='access_url')),
                ('bib_reference', models.TextField(blank=True, help_text='Bibcode or DOI preferred if available, or other bibliographic identifier or URL', null=True, verbose_name='bib_reference')),
                ('c1_resol_max', models.FloatField(blank=True, help_text='Resolution in the first coordinate, upper limit', null=True, verbose_name='c1_resol_max')),
                ('c1_resol_min', models.FloatField(blank=True, help_text='Resolution in the first coordinate, lower limit.', null=True, verbose_name='c1_resol_min')),
                ('c1max', models.FloatField(blank=True, help_text='Longitude on body, upper limit', null=True, verbose_name='c1max')),
                ('c1min', models.FloatField(blank=True, help_text='Longitude on body, lower limit.', null=True, verbose_name='c1min')),
                ('c2_resol_max', models.FloatField(blank=True, help_text='Resolution in the second coordinate, upper limit', null=True, verbose_name='c2_resol_max')),
                ('c2_resol_min', models.FloatField(blank=True, help_text='Resolution in the second coordinate, lower limit.', null=True, verbose_name='c2_resol_min')),
                ('c2max', models.FloatField(blank=True, help_text='Latitude on body, upper limit', null=True, verbose_name='c2max')),
                ('c2min', models.FloatField(blank=True, help_text='Latitude on body, lower limit.', null=True, verbose_name='c2min')),
                ('c3_resol_max', models.FloatField(blank=True, help_text='Resolution in the third coordinate, upper limit', null=True, verbose_name='c3_resol_max')),
                ('c3_resol_min', models.FloatField(blank=True, help_text='Resolution in the third coordinate, lower limit.', null=True, verbose_name='c3_resol_min')),
                ('c3max', models.FloatField(blank=True, help_text='Altitude from reference surface, upper limit', null=True, verbose_name='c3max')),
                ('c3min', models.FloatField(blank=True, help_text='Altitude from reference surface, lower limit.', null=True, verbose_name='c3min')),
                ('creation_date', models.DateTimeField(blank=True, help_text='Date of first entry of this granule', null=True, verbose_name='creation_date')),
                ('dataproduct_type', models.TextField(blank=True, help_text="The high-level organization of the data product, from a controlled vocabulary (e.g., 'im' for image, sp for spectrum). Multiple terms may be used, separated by # characters.", null=True, verbose_name='dataproduct_type')),
                ('emergence_max', models.FloatField(blank=True, help_text='Emergence angle during data acquisition, upper limit', null=True, verbose_name='emergence_max')),
                ('emergence_min', models.FloatField(blank=True, help_text='Emergence angle during data acquisition, lower limit.', null=True, verbose_name='emergence_min')),
                ('file_name', models.TextField(blank=True, help_text='Name of the data file only, case sensitive', null=True, verbose_name='file_name')),
                ('granule_gid', models.TextField(blank=True, help_text='Common to granules of same type (e.g. same map projection, or geometry data products). Can be alphanumeric.', null=True, verbose_name='granule_gid')),
                ('granule_uid', models.TextField(blank=True, help_text='Internal table row index, which must be unique within the table. Can be alphanumeric.', null=True, verbose_name='granule_uid')),
                ('incidence_max', models.FloatField(blank=True, help_text='Incidence angle (solar zenithal angle) during data acquisition, upper limit', null=True, verbose_name='incidence_max')),
                ('incidence_min', models.FloatField(blank=True, help_text='Incidence angle (solar zenithal angle) during data acquisition, lower limit.', null=True, verbose_name='incidence_min')),
                ('instrument_host_name', models.TextField(blank=True, help_text='Standard name of the observatory or spacecraft', null=True, verbose_name='instrument_host_name')),
                ('instrument_name', models.TextField(blank=True, help_text='Standard name of instrument', null=True, verbose_name='instrument_name')),
                ('measurement_type', models.TextField(blank=True, help_text='UCD(s) defining the data, with multiple entries separated by hash (#) characters.', null=True, verbose_name='measurement_type')),
                ('modification_date', models.DateTimeField(blank=True, help_text='Date of last modification (used to handle mirroring)', null=True, verbose_name='modification_date')),
                ('obs_id', models.TextField(blank=True, help_text='Associates granules derived from the same data (e.g. various representations/processing levels). Can be alphanumeric, may be the ID of original observation.', null=True, verbose_name='obs_id')),
                ('phase_max', models.FloatField(blank=True, help_text='Phase angle during data acquisition, upper limit', null=True, verbose_name='phase_max')),
                ('phase_min', models.FloatField(blank=True, help_text='Phase angle during data acquisition, lower limit.', null=True, verbose_name='phase_min')),
                ('processing_level', models.BigIntegerField(blank=True, help_text='Dataset-related encoding, or simplified CODMAC calibration level', null=True, verbose_name='processing_level')),
                ('publisher', models.TextField(blank=True, help_text='A short string identifying the entity running the data service used', null=True, verbose_name='publisher')),
                ('release_date', models.DateTimeField(blank=True, help_text='Start of public access period', null=True, verbose_name='release_date')),
                ('s_region', models.TextField(blank=True, help_text='ObsCore-like footprint, valid for celestial, spherical, or body-fixed frames', null=True, verbose_name='s_region')),
                ('service_title', models.TextField(blank=True, help_text='Title of resource (an acronym really, will be used to handle multiservice results)', null=True, verbose_name='service_title')),
                ('spatial_coordinate_description', models.TextField(blank=True, help_text='ID or specific coordinate system and version', null=True, verbose_name='spatial_coordinate_description')),
                ('spatial_frame_type', models.TextField(blank=True, help_text="Flavor of coordinate system, defines the nature of coordinates. From a controlled vocabulary, where 'none' means undefined.", null=True, verbose_name='spatial_frame_type')),
                ('spatial_origin', models.TextField(blank=True, help_text='Defines the frame origin', null=True, verbose_name='spatial_origin')),
                ('spectral_range_max', models.FloatField(blank=True, help_text='Spectral range (frequency), upper limit', null=True, verbose_name='spectral_range_max')),
                ('spectral_range_min', models.FloatField(blank=True, help_text='Spectral range (frequency), lower limit.', null=True, verbose_name='spectral_range_min')),
                ('spectral_resolution_max', models.FloatField(blank=True, help_text='Spectral resolution, upper limit', null=True, verbose_name='spectral_resolution_max')),
                ('spectral_resolution_min', models.FloatField(blank=True, help_text='Spectral resolution, lower limit.', null=True, verbose_name='spectral_resolution_min')),
                ('spectral_sampling_step_max', models.FloatField(blank=True, help_text='Spectral sampling step, upper limit', null=True, verbose_name='spectral_sampling_step_max')),
                ('spectral_sampling_step_min', models.FloatField(blank=True, help_text='Spectral sampling step, lower limit.', null=True, verbose_name='spectral_sampling_step_min')),
                ('target_class', models.TextField(blank=True, help_text='Type of target, from a controlled vocabulary.', null=True, verbose_name='target_class')),
                ('target_name', models.TextField(blank=True, help_text='Standard IAU name of target (from a list related to target class), case sensitive', null=True, verbose_name='target_name')),
                ('thumbnail_url', models.TextField(blank=True, help_text='URL of a thumbnail image with predefined size (png ~200 pix, for use in a client only)', null=True, verbose_name='thumbnail_url')),
                ('time_exp_max', models.FloatField(blank=True, help_text='Integration time of the measurement, upper limit', null=True, verbose_name='time_exp_max')),
                ('time_exp_min', models.FloatField(blank=True, help_text='Integration time of the measurement, lower limit.', null=True, verbose_name='time_exp_min')),
                ('time_max', models.FloatField(blank=True, help_text='Acquisition stop time (in JD), as UTC at time_refposition', null=True, verbose_name='time_max')),
                ('time_min', models.FloatField(blank=True, help_text='Acquisition start time (in JD), as UTC at time_refposition', null=True, verbose_name='time_min')),
                ('time_sampling_step_max', models.FloatField(blank=True, help_text='Sampling time for measurements of dynamical phenomena, upper limit', null=True, verbose_name='time_sampling_step_max')),
                ('time_sampling_step_min', models.FloatField(blank=True, help_text='Sampling time for measurements of dynamical phenomena, lower limit.', null=True, verbose_name='time_sampling_step_min')),
                ('time_scale', models.TextField(blank=True, help_text='Defaults to UTC in data services; takes values from http://www.ivoa.net/rdf/time_scale otherwise', null=True, verbose_name='time_scale')),
                ('data_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadata_chrotellevel1', to='dataset.datalocation')),
                ('tags', models.ManyToManyField(blank=True, related_name='metadata_chrotellevel1', to='metadata.Tag')),
            ],
            options={
                'verbose_name': 'ChroTel level 1 metadata',
                'verbose_name_plural': 'ChroTel level 1 metadata',
                'ordering': ['date_beg'],
                'abstract': False,
            },
        ),
    ]
