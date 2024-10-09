# Generated by Django 5.0.9 on 2024-10-09 14:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SMTP',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'InActive')], default='active', max_length=30)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_name', models.CharField(help_text='Name of the sender', max_length=250)),
                ('host', models.CharField(max_length=250)),
                ('port', models.PositiveIntegerField()),
                ('username', models.CharField(help_text='Email address of the sender', max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('use_tls', models.BooleanField(default=False)),
                ('use_ssl', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
