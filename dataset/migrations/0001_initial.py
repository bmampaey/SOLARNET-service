import dataset.models.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Telescope',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='Telescope description', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='Instrument description', null=True)),
                ('telescope', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='instruments', to='dataset.telescope')),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Can contain any unicode character', max_length=200, unique=True)),
                ('description', models.TextField(blank=True, help_text='Can contain html with links, emphasis, etc.', null=True)),
                ('contact_email', models.EmailField(blank=True, help_text='Email of the dataset archive contact person', max_length=254, null=True)),
                ('archive_url', models.URLField(blank=True, help_text='Official URL of the dataset archive', max_length=2000, null=True)),
                ('characteristics', models.ManyToManyField(blank=True, related_name='datasets', to='dataset.Characteristic')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='datasets', to='dataset.instrument')),
                ('metadata_content_type', models.OneToOneField(blank=True, help_text='The model for this dataset metadata', limit_choices_to=models.Q(('app_label', 'metadata'), models.Q(('model', 'tag'), _negated=True)), null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('telescope', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='datasets', to='dataset.telescope')),
                ('user_group', models.ForeignKey(blank=True, help_text='User of this group can modify the dataset', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_groups', to='auth.group')),
            ],
            options={
                'verbose_name': 'Dataset',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the corresponding field in the metadata model, can contain only letters, digits and underscore', max_length=200, validators=[dataset.models.validators.valid_keyword_name])),
                ('verbose_name', models.CharField(help_text='Verbose name of the keyword, can contain any unicode character', max_length=200)),
                ('type', models.CharField(choices=[('text', 'text'), ('boolean', 'boolean'), ('integer', 'integer'), ('real', 'real'), ('time (ISO 8601)', 'time (ISO 8601)')], default='text', help_text='Python type of the keyword', max_length=15)),
                ('unit', models.CharField(blank=True, help_text='Physical unit (SI compliant) of the keyword', max_length=30, null=True)),
                ('description', models.TextField(blank=True, help_text='Full description of the keyword', null=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='dataset.dataset')),
            ],
            options={
                'ordering': ['dataset', 'name'],
                'unique_together': {('dataset', 'name'), ('dataset', 'verbose_name')},
            },
        ),
        migrations.CreateModel(
            name='DataLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.URLField(help_text='URL of the data file at the remote site', max_length=2000, verbose_name='File URL')),
                ('file_size', models.PositiveBigIntegerField(help_text='Size of the data file in bytes')),
                ('file_path', models.TextField(db_index=True, help_text='File name or relative path of the data file, use / as the path separator and avoid the characters \\:*?"\\\'<>|\\r\\n\\0', validators=[dataset.models.validators.valid_file_path])),
                ('thumbnail_url', models.URLField(blank=True, help_text='URL of the thumbnail image at the remote site', max_length=2000, null=True, verbose_name='Thumbnail URL')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='Date of last update')),
                ('offline', models.BooleanField(default=False, help_text='The data is not available for download')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_locations', to='dataset.dataset')),
            ],
            options={
                'unique_together': {('dataset', 'file_url'), ('dataset', 'file_path')},
            },
        ),
    ]
