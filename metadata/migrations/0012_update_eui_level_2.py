from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0011_update_eui_level_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='euilevel2',
            name='gcount',
            field=models.BigIntegerField(blank=True, help_text='number of groups', null=True, verbose_name='GCOUNT'),
        ),
        migrations.AddField(
            model_name='euilevel2',
            name='pcount',
            field=models.BigIntegerField(blank=True, help_text='number of group parameters', null=True, verbose_name='PCOUNT'),
        ),
        migrations.AlterField(
            model_name='euilevel2',
            name='doorpos',
            field=models.BigIntegerField(blank=True, help_text='Door position (raw)', null=True, verbose_name='DOORPOS'),
        ),
        migrations.AlterField(
            model_name='euilevel2',
            name='filtpos',
            field=models.BigIntegerField(blank=True, help_text='(0-199) filter wheel position service5', null=True, verbose_name='FILTPOS'),
        ),
        migrations.AlterField(
            model_name='euilevel2',
            name='naxis',
            field=models.BigIntegerField(blank=True, help_text='number of axes in data cube', null=True, verbose_name='NAXIS'),
        ),
        migrations.AlterField(
            model_name='euilevel2',
            name='naxis1',
            field=models.BigIntegerField(blank=True, help_text='length of data axis 1', null=True, verbose_name='NAXIS1'),
        ),
        migrations.AlterField(
            model_name='euilevel2',
            name='naxis2',
            field=models.BigIntegerField(blank=True, help_text='length of data axis 2', null=True, verbose_name='NAXIS2'),
        ),
        migrations.AlterField(
            model_name='euilevel2',
            name='vers_sw',
            field=models.TextField(blank=True, help_text='(L1) version of SW that provided FITS file', null=True, verbose_name='VERS_SW'),
        ),
        migrations.AlterField(
            model_name='euilevel2',
            name='version',
            field=models.TextField(blank=True, help_text='incremental version number', null=True, verbose_name='VERSION'),
        ),
        migrations.AlterField(
            model_name='euilevel2',
            name='wavelnth',
            field=models.BigIntegerField(blank=True, help_text='characteristic wavelength observation', null=True, verbose_name='WAVELNTH'),
        ),
    ]
