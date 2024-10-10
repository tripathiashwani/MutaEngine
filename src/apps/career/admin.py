from django.contrib import admin

from .models.applicant import JobApplicant, JobApplicantExtraField
from .models.job import (
    JobApplicantTemplate,
    JobAssignmentTemplate, 
    JobTemplate, 
    OfferTemplate, 
    TemplateExtraField
)

admin.site.register(JobApplicant)

admin.site.register(JobApplicantExtraField)

admin.site.register(JobApplicantTemplate)

admin.site.register(JobAssignmentTemplate)

admin.site.register(JobTemplate)

admin.site.register(OfferTemplate)

admin.site.register(TemplateExtraField)