from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
        ('metadata', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aialevel1',
            options={'ordering': ['date_beg'], 'verbose_name': 'AIA level 1 metadata', 'verbose_name_plural': 'AIA level 1 metadata'},
        ),
        migrations.AlterModelOptions(
            name='chromis',
            options={'ordering': ['date_beg'], 'verbose_name': 'CHROMIS metadata', 'verbose_name_plural': 'CHROMIS metadata'},
        ),
        migrations.AlterModelOptions(
            name='chrotel',
            options={'ordering': ['date_beg'], 'verbose_name': 'ChroTel metadata', 'verbose_name_plural': 'ChroTel metadata'},
        ),
        migrations.AlterModelOptions(
            name='crisp',
            options={'ordering': ['date_beg'], 'verbose_name': 'CRISP metadata', 'verbose_name_plural': 'CRISP metadata'},
        ),
        migrations.AlterModelOptions(
            name='eitlevel0',
            options={'ordering': ['date_beg'], 'verbose_name': 'EIT level 0 metadata', 'verbose_name_plural': 'EIT level 0 metadata'},
        ),
        migrations.AlterModelOptions(
            name='grislevel1',
            options={'ordering': ['date_beg'], 'verbose_name': 'GRIS level 1 metadata', 'verbose_name_plural': 'GRIS level 1 metadata'},
        ),
        migrations.AlterModelOptions(
            name='hmimagnetogram',
            options={'ordering': ['date_beg'], 'verbose_name': 'HMI magnetogram metadata', 'verbose_name_plural': 'HMI magnetogram metadata'},
        ),
        migrations.AlterModelOptions(
            name='ibis',
            options={'ordering': ['date_beg'], 'verbose_name': 'IBIS metadata', 'verbose_name_plural': 'IBIS metadata'},
        ),
        migrations.AlterModelOptions(
            name='rosa',
            options={'ordering': ['date_beg'], 'verbose_name': 'ROSA metadata', 'verbose_name_plural': 'ROSA metadata'},
        ),
        migrations.AlterModelOptions(
            name='swaplevel1',
            options={'ordering': ['date_beg'], 'verbose_name': 'SWAP level 1 metadata', 'verbose_name_plural': 'SWAP level 1 metadata'},
        ),
        migrations.AlterModelOptions(
            name='themis',
            options={'ordering': ['date_beg'], 'verbose_name': 'Themis metadata', 'verbose_name_plural': 'Themis metadata'},
        ),
        migrations.AlterModelOptions(
            name='xrt',
            options={'ordering': ['date_beg'], 'verbose_name': 'XRT metadata', 'verbose_name_plural': 'XRT metadata'},
        ),
        migrations.CreateModel(
            name='LyraLevel2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.TextField(db_index=True, help_text='Unique identification string for the observation metadata, usually in the form YYYYMMDDHHMMSS; cannot be modified once it is set', unique=True, verbose_name='Observation ID')),
                ('fits_header', models.TextField(blank=True, null=True)),
                ('date_beg', models.DateTimeField(blank=True, db_index=True, help_text='Start time of the observation [UTC]', null=True, verbose_name='DATE-BEG')),
                ('date_end', models.DateTimeField(blank=True, db_index=True, help_text='End time of the observation [UTC]', null=True, verbose_name='DATE-END')),
                ('wavemin', models.FloatField(blank=True, db_index=True, help_text='Min value of the observation spectral range [nm]', null=True, verbose_name='WAVEMIN')),
                ('wavemax', models.FloatField(blank=True, db_index=True, help_text='Max value of the observation spectral range [nm]', null=True, verbose_name='WAVEMAX')),
                ('algor_v', models.TextField(blank=True, help_text='LYRA calibration S/W version', null=True, verbose_name='ALGOR_V')),
                ('datasrc', models.TextField(blank=True, help_text='receiving ground station', null=True, verbose_name='DATASRC')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='DATE')),
                ('date_obs', models.DateTimeField(blank=True, help_text='UTC start of observation', null=True, verbose_name='DATE-OBS')),
                ('filename', models.TextField(blank=True, help_text='name of this FITS file', null=True, verbose_name='FILENAME')),
                ('instrume', models.TextField(blank=True, null=True, verbose_name='INSTRUME')),
                ('level', models.BigIntegerField(blank=True, help_text='calibration level', null=True, verbose_name='LEVEL')),
                ('naxis', models.BigIntegerField(blank=True, null=True, verbose_name='NAXIS')),
                ('object', models.TextField(blank=True, null=True, verbose_name='OBJECT')),
                ('obs_mode', models.TextField(blank=True, help_text='science data', null=True, verbose_name='OBS_MODE')),
                ('origin', models.TextField(blank=True, null=True, verbose_name='ORIGIN')),
                ('telescop', models.TextField(blank=True, null=True, verbose_name='TELESCOP')),
                ('data_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metadata_lyralevel2', to='dataset.datalocation')),
                ('tags', models.ManyToManyField(blank=True, related_name='metadata_lyralevel2', to='metadata.Tag')),
            ],
            options={
                'verbose_name': 'LYRA level 2 metadata',
                'verbose_name_plural': 'LYRA level 2 metadata',
                'ordering': ['date_beg'],
                'abstract': False,
            },
        ),
    ]
