from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0015_update_xrt'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Themis',
        ),
    ]
