from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0014_update_xrt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xrt',
            name='e_fw1_p',
            field=models.TextField(blank=True, help_text='Filter Wheel 1 position', null=True, verbose_name='E_FW1_P'),
        ),
        migrations.AlterField(
            model_name='xrt',
            name='e_fw2_p',
            field=models.TextField(blank=True, help_text='Filter Wheel 2 position', null=True, verbose_name='E_FW2_P'),
        ),
        migrations.AlterField(
            model_name='xrt',
            name='expmpas',
            field=models.TextField(blank=True, help_text='Single or multipass exposure', null=True, verbose_name='EXPMPAS'),
        ),
        migrations.AlterField(
            model_name='xrt',
            name='orig_rf1',
            field=models.TextField(blank=True, null=True, verbose_name='ORIG_RF1'),
        ),
        migrations.AlterField(
            model_name='xrt',
            name='sci_obj',
            field=models.TextField(blank=True, help_text='Up to 5 target phenomena selected from list.', null=True, verbose_name='SCI_OBJ'),
        ),
        migrations.AlterField(
            model_name='xrt',
            name='sci_obs',
            field=models.TextField(blank=True, help_text='Target phenomena.', null=True, verbose_name='SCI_OBS'),
        ),
    ]
