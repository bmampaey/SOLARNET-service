from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0013_update_eit_level_0'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xrt',
            name='ctime',
            field=models.TextField(blank=True, help_text='Same value as DATE OBS, but in a different format', null=True, verbose_name='CTIME'),
        ),
    ]
