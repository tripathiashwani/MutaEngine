from django.db import models

from src.apps.common.models import BaseModel
from src.apps.common.utils import get_upload_folder
from src.apps.career.models.job import JobTemplate, TemplateExtraField

class JobApplicant(BaseModel):
    job_template = models.ForeignKey(JobTemplate, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    total_yoe = models.CharField(max_length=10, help_text="Total years of experience")
    skills = models.CharField(max_length=255, help_text="Comma-separated skills")
    linkedin = models.URLField()
    resume = models.FileField(upload_to=get_upload_folder)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class JobApplicantExtraField(BaseModel):
    job_applicant = models.ForeignKey(JobApplicant, on_delete=models.CASCADE)
    template_extra_field = models.ForeignKey(TemplateExtraField, on_delete=models.CASCADE)
    value = models.JSONField()

    def __str__(self):
        return f"Extra Field for {self.job_applicant.first_name} {self.job_applicant.last_name}"


class AssignmentSubmission(BaseModel):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    applicant_id = models.UUIDField()
    deployment_url = models.URLField()
    project_github_url = models.URLField()
    video_url = models.URLField()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} assignment submission'   