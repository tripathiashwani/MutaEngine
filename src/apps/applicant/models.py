from django.db import models

from src.apps.common.models import BaseModel

class JobApplicant(BaseModel):
    job_template = models.ForeignKey('JobManagement.JobTemplate', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    total_yoe = models.CharField(max_length=10, help_text="Total years of experience")
    skills = models.CharField(max_length=255, help_text="Comma-separated skills")
    linkedin = models.URLField()
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class JobApplicantExtraField(BaseModel):
    job_applicant = models.ForeignKey(JobApplicant, on_delete=models.CASCADE)
    template_extra_field = models.ForeignKey('TemplateManagement.TemplateExtraField', on_delete=models.CASCADE)
    value = models.JSONField()

    def __str__(self):
        return f"Extra Field for {self.job_applicant.first_name} {self.job_applicant.last_name}"
