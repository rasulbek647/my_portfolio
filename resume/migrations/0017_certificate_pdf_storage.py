# Migration corrected: revert document field back to plain FileField (no custom storage)
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0016_add_service_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='certificates/docs/', verbose_name='Document (PDF)'),
        ),
    ]
