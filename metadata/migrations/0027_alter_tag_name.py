# Generated by Django 3.2.4 on 2021-06-24 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0026_upgrade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
