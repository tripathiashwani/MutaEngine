# Generated by Django 5.1.2 on 2024-10-22 12:40

import django.db.models.deletion
import django_ckeditor_5.fields
import src.apps.common.utils
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
            name="AssignmentSubmission",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "InActive")],
                        default="active",
                        max_length=30,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("applicant_id", models.UUIDField()),
                ("deployment_url", models.URLField()),
                ("project_github_url", models.URLField()),
                ("video_url", models.URLField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="JobApplicantTemplate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "InActive")],
                        default="active",
                        max_length=30,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="JobAssignmentTemplate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "InActive")],
                        default="active",
                        max_length=30,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                (
                    "content",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="content"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OfferTemplate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "InActive")],
                        default="active",
                        max_length=30,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                (
                    "content",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="content"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TemplateExtraField",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "InActive")],
                        default="active",
                        max_length=30,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("label", models.CharField(max_length=255)),
                (
                    "field_type",
                    models.CharField(
                        choices=[
                            ("text", "Text"),
                            ("textarea", "Textarea"),
                            ("checkbox", "Checkbox"),
                            ("radio", "Radio"),
                            ("select", "Select"),
                            ("rich_text", "Rich_Text"),
                        ],
                        default="text",
                        max_length=50,
                    ),
                ),
                ("required", models.BooleanField(default=False)),
                ("options", models.JSONField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="JobTemplate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "InActive")],
                        default="active",
                        max_length=30,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(blank=True, max_length=150, unique=True)),
                (
                    "work_location",
                    models.CharField(
                        choices=[
                            ("onsite", "Onsite"),
                            ("remote", "Remote"),
                            ("hybrid", "Hybrid"),
                        ],
                        default="onsite",
                        max_length=255,
                    ),
                ),
                (
                    "work_type",
                    models.CharField(
                        choices=[
                            ("full_time", "Full_Time"),
                            ("part_time", "Part_Time"),
                            ("contract", "Contract"),
                            ("internship", "Internship"),
                        ],
                        default="full_time",
                        max_length=255,
                    ),
                ),
                ("position", models.CharField(max_length=255)),
                ("department", models.CharField(max_length=255)),
                (
                    "description",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="description"),
                ),
                ("deadline", models.DateField()),
                ("ctc", models.CharField(max_length=255)),
                (
                    "job_applicant_template",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="career.jobapplicanttemplate",
                    ),
                ),
                (
                    "job_assignment_template",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="career.jobassignmenttemplate",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "offer_template",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="career.offertemplate",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="JobApplicant",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "InActive")],
                        default="active",
                        max_length=30,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=15)),
                (
                    "total_yoe",
                    models.CharField(
                        help_text="Total years of experience", max_length=10
                    ),
                ),
                (
                    "skills",
                    models.CharField(
                        help_text="Comma-separated skills", max_length=255
                    ),
                ),
                ("linkedin", models.URLField()),
                (
                    "resume",
                    models.FileField(upload_to=src.apps.common.utils.get_upload_folder),
                ),
                (
                    "job_template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="career.jobtemplate",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="jobapplicanttemplate",
            name="template_extra_fields",
            field=models.ManyToManyField(to="career.templateextrafield"),
        ),
        migrations.CreateModel(
            name="JobApplicantExtraField",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "InActive")],
                        default="active",
                        max_length=30,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("value", models.JSONField()),
                (
                    "job_applicant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="career.jobapplicant",
                    ),
                ),
                (
                    "template_extra_field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="career.templateextrafield",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
