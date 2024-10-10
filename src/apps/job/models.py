from django.db import models

from src.apps.common.models import BaseModel

class JobApplicantTemplate(BaseModel):
    title = models.CharField(max_length=255)
    template_extra_fields = models.ManyToManyField('TemplateManagement.TemplateExtraField')

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

class JobTemplate(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    work_location = models.CharField(max_length=255, choices=[('onsite', 'Onsite'), ('remote', 'Remote'), ('hybrid', 'Hybrid')])
    position = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey('UserManagement.User', on_delete=models.CASCADE)
    deadline = models.DateField()
    ctc = models.CharField(max_length=255)
    job_applicant_template = models.ForeignKey(JobApplicantTemplate, on_delete=models.SET_NULL, null=True)
    job_assignment_template = models.ForeignKey(JobAssignmentTemplate, on_delete=models.SET_NULL, null=True)
    offer_template = models.ForeignKey(OfferTemplate, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
