# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-08 10:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DataLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.TextField(blank=True, help_text='URL of the data at the remote site.', max_length=255, null=True, unique=True, validators=[django.core.validators.URLValidator()])),
                ('file_size', models.IntegerField(blank=True, default=0, help_text='Size of the data in bytes.', null=True)),
                ('thumbnail_url', models.TextField(blank=True, default=None, help_text='URL of the thumbnail at the remote site.', max_length=255, null=True, validators=[django.core.validators.URLValidator()])),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date of last update')),
            ],
            options={
                'db_table': 'data_location',
            },
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.TextField(max_length=20, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[a-z][_a-z0-9]*$')], verbose_name='Dataset id.')),
                ('name', models.TextField(max_length=40, unique=True, verbose_name='Dataset display name.')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Dataset description')),
                ('contact', models.TextField(blank=True, help_text='Contact email for the data set.', max_length=50, null=True, validators=[django.core.validators.EmailValidator()])),
                ('_metadata_model', models.OneToOneField(blank=True, help_text='The model for this dataset metadata', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
                ('characteristics', models.ManyToManyField(blank=True, related_name='datasets', to='dataset.Characteristic')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'dataset',
                'verbose_name': 'Dataset',
                'verbose_name_plural': 'Datasets',
            },
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('name', models.TextField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='Instrument description', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_column', models.TextField(max_length=30, validators=[django.core.validators.RegexValidator('^[a-z][_a-z]*$')], verbose_name='Column name of the corresponding keyword in the metadata table.')),
                ('name', models.CharField(help_text='Fits like name of the keyword. Can contain space and dashes.', max_length=70)),
                ('python_type', models.CharField(choices=[('str', 'string'), ('bool', 'bool'), ('int', 'int'), ('float', 'float'), ('datetime', 'datetime (iso format)')], default='string', help_text='Python type of the keyword.', max_length=12)),
                ('unit', models.CharField(blank=True, help_text='Physical unit (SI compliant) of the keyword.', max_length=10, null=True)),
                ('description', models.TextField(blank=True, help_text='Full description of the keyword.', max_length=70, null=True)),
                ('dataset', models.ForeignKey(db_column='dataset', on_delete=django.db.models.deletion.DO_NOTHING, related_name='keywords', to='dataset.Dataset')),
            ],
            options={
                'ordering': ['dataset', 'db_column'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.TextField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='Telescope',
            fields=[
                ('name', models.TextField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='Telescope description', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='instrument',
            name='telescope',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='instruments', to='dataset.Telescope'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='instrument',
            field=models.ForeignKey(db_column='instrument', on_delete=django.db.models.deletion.DO_NOTHING, related_name='datasets', to='dataset.Instrument'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='telescope',
            field=models.ForeignKey(db_column='telescope', on_delete=django.db.models.deletion.DO_NOTHING, related_name='datasets', to='dataset.Telescope'),
        ),
        migrations.AlterUniqueTogether(
            name='keyword',
            unique_together=set([('dataset', 'db_column'), ('dataset', 'name')]),
        ),
    ]
