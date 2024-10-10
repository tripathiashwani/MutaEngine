from django.db import models

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
    content = models.TextField()

    def __str__(self):
        return self.title

class OfferTemplate(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


class WorkLocationChoices(models.TextChoices):
    ONSITE = 'onsite', 'Onsite'
    REMOTE = 'remote', 'Remote'
    HYBRID = 'hybrid', 'Hybrid'


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
    position = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    ctc = models.CharField(max_length=255)
    job_applicant_template = models.ForeignKey(JobApplicantTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    job_assignment_template = models.ForeignKey(JobAssignmentTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    offer_template = models.ForeignKey(OfferTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
