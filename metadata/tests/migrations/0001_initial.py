from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dataset', '0001_initial'),
        ('metadata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseMetadataTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.TextField(db_index=True, help_text='Unique identification string for the observation metadata, usually in the form YYYYMMDDHHMMSS; cannot be modified once it is set', unique=True, verbose_name='Observation ID')),
                ('fits_header', models.TextField(blank=True, null=True)),
                ('date_beg', models.DateTimeField(blank=True, db_index=True, help_text='Start time of the observation [UTC]', null=True, verbose_name='DATE-BEG')),
                ('date_end', models.DateTimeField(blank=True, db_index=True, help_text='End time of the observation [UTC]', null=True, verbose_name='DATE-END')),
                ('wavemin', models.FloatField(blank=True, db_index=True, help_text='Min value of the observation spectral range [nm]', null=True, verbose_name='WAVEMIN')),
                ('wavemax', models.FloatField(blank=True, db_index=True, help_text='Max value of the observation spectral range [nm]', null=True, verbose_name='WAVEMAX')),
                ('data_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tests_basemetadatatest', to='dataset.datalocation')),
                ('tags', models.ManyToManyField(blank=True, related_name='tests_basemetadatatest', to='metadata.Tag')),
            ],
            options={
                'ordering': ['date_beg'],
                'abstract': False,
            },
        ),
    ]
