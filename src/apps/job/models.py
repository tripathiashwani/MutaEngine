from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

from src.apps.common.models import BaseModel
from src.apps.auth.models import UserModelMixin, User

class TemplateExtraFieldType(models.TextChoices):
    TEXT = 'text', 'Text'
    TEXTAREA = 'textarea', 'Textarea'
    CHECKBOX = 'checkbox', 'Checkbox'
    RADIO = 'radio', 'Radio'
    SELECT = 'select', 'Select'
    RICH_TEXT = 'rich text', 'Rich Text'

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
    title = models.CharField(max_length=255,null=True, blank=True)
    content = CKEditor5Field('content', config_name='extends',null=True, blank=True)
    author = models.CharField(max_length=255,null=True, blank=True) 
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    manager=models.ForeignKey(User, on_delete=models.CASCADE, related_name='offer_templates',null=True, blank=True)
    joining_date = models.DateField(blank=True,null=True )  
    html_content = models.TextField(null=True, blank=True)



    def __str__(self):
        return self.title


class WorkLocationChoices(models.TextChoices):
    ONSITE = 'onsite', 'Onsite'
    REMOTE = 'remote', 'Remote'
    HYBRID = 'hybrid', 'Hybrid'


class WorkType(models.TextChoices):
    FULL_TIME = 'full time', 'Full Time'
    PART_TIME = 'part time', 'Part Time'
    CONTRACT = 'contract', 'Contract'
    INTERNSHIP = 'internship', 'Internship'

class JobTemplate(BaseModel,UserModelMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=150, blank=True)
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
    department = models.CharField(max_length=255)
    experience = models.CharField(max_length=255, null=True, blank=True)
    country_location = models.CharField(max_length=255, default="India")
    description = CKEditor5Field('description', config_name='extends')
    deadline = models.DateTimeField()
    ctc = models.CharField(max_length=255)
    job_applicant_template = models.ForeignKey(JobApplicantTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    job_assignment_template = models.ForeignKey(JobAssignmentTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    offer_template = models.ForeignKey(OfferTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.title))
        return super().save(*args, **kwargs)
