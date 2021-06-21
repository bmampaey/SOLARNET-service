# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-18 09:49
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('web_account', '0001_initial'),
        ('dataset', '0003_auto_20160321_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_string', models.TextField(blank=True, help_text='Query string for the data selection', max_length=2000, null=True)),
                ('metadata_oids', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(help_text='Unique identifier for the observation metadata, usually in the form YYYYMMDDHHMMSS', verbose_name='Observation ID'), blank=True, help_text='List of metadata oids', null=True, size=None)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date of creation')),
                ('number_items', models.IntegerField(blank=True, help_text='Number of items in the data selection', null=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasets', related_query_name='dataset', to='dataset.Dataset')),
            ],
            options={
                'db_table': 'data_selection',
            },
        ),
        migrations.CreateModel(
            name='UserDataSelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the data selection', max_length=80)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date of creation')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date of last update')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_account.User')),
            ],
            options={
                'ordering': ['-updated'],
                'db_table': 'user_data_selection',
                'get_latest_by': 'updated',
            },
        ),
        migrations.AddField(
            model_name='dataselection',
            name='user_data_selection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_selections', to='data_selection.UserDataSelection'),
        ),
        migrations.AlterUniqueTogether(
            name='userdataselection',
            unique_together=set([('user', 'name')]),
        ),
    ]
