# Generated by Django 5.0.2 on 2024-10-29 11:09

import src.apps.common.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0005_jobapplicant_joining_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplicant',
            name='resume',
            field=models.FileField(null=True, upload_to=src.apps.common.utils.get_upload_folder),
        ),
    ]
