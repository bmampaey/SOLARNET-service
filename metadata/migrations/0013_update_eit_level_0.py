from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0012_update_eui_level_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eitlevel0',
            name='commanded_exposure_time',
            field=models.FloatField(blank=True, null=True, verbose_name='COMMANDED_EXPOSURE_TIME'),
        ),
        migrations.AlterField(
            model_name='eitlevel0',
            name='shutter_close_time',
            field=models.FloatField(blank=True, null=True, verbose_name='SHUTTER_CLOSE_TIME'),
        ),
    ]
