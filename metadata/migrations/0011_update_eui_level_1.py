from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0010_add_gaia_dem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='euilevel1',
            name='extend',
        ),
        migrations.AddField(
            model_name='euilevel1',
            name='gcount',
            field=models.BigIntegerField(blank=True, help_text='number of groups', null=True, verbose_name='GCOUNT'),
        ),
        migrations.AddField(
            model_name='euilevel1',
            name='pcount',
            field=models.BigIntegerField(blank=True, help_text='number of group parameters', null=True, verbose_name='PCOUNT'),
        ),
        migrations.AlterField(
            model_name='euilevel1',
            name='bscale',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='BSCALE'),
        ),
        migrations.AlterField(
            model_name='euilevel1',
            name='bzero',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='BZERO'),
        ),
        migrations.AlterField(
            model_name='euilevel1',
            name='doorpos',
            field=models.BigIntegerField(blank=True, help_text='Door position (raw)', null=True, verbose_name='DOORPOS'),
        ),
        migrations.AlterField(
            model_name='euilevel1',
            name='filtpos',
            field=models.BigIntegerField(blank=True, help_text='(0-199) filter wheel position service5', null=True, verbose_name='FILTPOS'),
        ),
        migrations.AlterField(
            model_name='euilevel1',
            name='parent',
            field=models.TextField(blank=True, help_text='source file curre', null=True, verbose_name='PARENT'),
        ),
        migrations.AlterField(
            model_name='euilevel1',
            name='vers_sw',
            field=models.TextField(blank=True, help_text='version of SW that provided FITS file', null=True, verbose_name='VERS_SW'),
        ),
        migrations.AlterField(
            model_name='euilevel1',
            name='version',
            field=models.TextField(blank=True, help_text='incremental version number', null=True, verbose_name='VERSION'),
        ),
        migrations.AlterField(
            model_name='euilevel1',
            name='wavelnth',
            field=models.BigIntegerField(blank=True, help_text='characteristic wavelength observation', null=True, verbose_name='WAVELNTH'),
        ),
    ]
