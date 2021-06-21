# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-03-24 14:04
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0010_datalocation_offline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='db_column',
            field=models.TextField(max_length=30, validators=[django.core.validators.RegexValidator('^[a-z][_a-z0-9]*$')], verbose_name='Column name of the corresponding keyword in the metadata table.'),
        ),
    ]
