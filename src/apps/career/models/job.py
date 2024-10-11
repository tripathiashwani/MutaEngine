from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from src.apps.common.models import BaseModel
from src.apps.auth.models import UserModelMixin

class TemplateExtraFieldType(models.TextChoices):
    TEXT = 'text', 'Text'
    TEXTAREA = 'textarea', 'Textarea'
    CHECKBOX = 'checkbox', 'Checkbox'
    RADIO = 'radio', 'Radio'
    SELECT = 'select', 'Select'
    RICH_TEXT = 'rich_text', 'Rich_Text'

class TemplateExtraField(BaseModel):
    label = models.CharField(max_length=255)
    field_type = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=TemplateExtraFieldType.choices,
        default=TemplateExtraFieldType.TEXT,
    )
    required = models.BooleanField(default=False)
    options = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.label

class JobApplicantTemplate(BaseModel):
    title = models.CharField(max_length=255)
    template_extra_fields = models.ManyToManyField(TemplateExtraField)

    def __str__(self):
        return self.title

class JobAssignmentTemplate(BaseModel):
    title = models.CharField(max_length=255)
    content = CKEditor5Field('content', config_name='extends')

    def __str__(self):
        return self.title

class OfferTemplate(BaseModel):
    title = models.CharField(max_length=255)
    content = CKEditor5Field('content', config_name='extends')

    def __str__(self):
        return self.title


class WorkLocationChoices(models.TextChoices):
    ONSITE = 'onsite', 'Onsite'
    REMOTE = 'remote', 'Remote'
    HYBRID = 'hybrid', 'Hybrid'


class WorkType(models.TextChoices):
    FULL_TIME = 'full_time', 'Full_Time'
    PART_TIME = 'part_time', 'Part_Time'
    CONTRACT = 'contract', 'Contract'
    INTERNSHIP = 'internship', 'Internship'

class JobTemplate(BaseModel,UserModelMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    work_location = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=WorkLocationChoices.choices,
        default=WorkLocationChoices.ONSITE,
    )
    work_type = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=WorkType.choices,
        default=WorkType.FULL_TIME
    )
    position = models.CharField(max_length=255)
    description = CKEditor5Field('description', config_name='extends')
    deadline = models.DateField()
    ctc = models.CharField(max_length=255)
    job_applicant_template = models.ForeignKey(JobApplicantTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    job_assignment_template = models.ForeignKey(JobAssignmentTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    offer_template = models.ForeignKey(OfferTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
