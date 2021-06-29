from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_string', models.TextField(blank=True, null=True, verbose_name='Query string representing the dataset metadata selection')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description for the data selection')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('uuid', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, unique=True, verbose_name='Unique identifier for web access')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_selections', related_query_name='data_selection', to='dataset.dataset')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_selections', related_query_name='data_selection', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['owner', '-creation_time'],
            },
        ),
    ]
