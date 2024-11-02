# Generated by Django 5.0.2 on 2024-11-02 07:38

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0007_alter_jobassignmenttemplate_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobassignmenttemplate',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='jobtemplate',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='offertemplate',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content'),
        ),
    ]
