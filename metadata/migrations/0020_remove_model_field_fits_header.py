from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0019_delete_chrotel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aialevel1',
            name='fits_header',
        ),
        migrations.RemoveField(
            model_name='chrotellevel1',
            name='fits_header',
        ),
        migrations.RemoveField(
            model_name='eitsynoptic',
            name='fits_header',
        ),
        migrations.RemoveField(
            model_name='gaiadem',
            name='fits_header',
        ),
        migrations.RemoveField(
            model_name='grislevel1',
            name='fits_header',
        ),
        migrations.RemoveField(
            model_name='hmimagnetogram',
            name='fits_header',
        ),
        migrations.RemoveField(
            model_name='larslevel1',
            name='fits_header',
        ),
        migrations.RemoveField(
            model_name='rosa',
            name='fits_header',
        ),
    ]
