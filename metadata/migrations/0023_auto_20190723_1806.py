# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2019-07-23 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0022_auto_20190723_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crisp',
            name='date_avg',
            field=models.DateTimeField(blank=True, help_text='Average time of observation (provided va', null=True, verbose_name='DATE-AVG'),
        ),
        migrations.AlterField(
            model_name='crisp',
            name='date_obs',
            field=models.DateTimeField(blank=True, help_text='Inferred from directory.', null=True, verbose_name='DATE-OBS'),
        ),
        migrations.AlterField(
            model_name='crisp',
            name='startobs',
            field=models.DateTimeField(blank=True, null=True, verbose_name='STARTOBS'),
        ),
    ]
