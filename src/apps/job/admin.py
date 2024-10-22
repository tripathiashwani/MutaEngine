from django.contrib import admin

from .models import (
    JobApplicantTemplate,
    JobAssignmentTemplate, 
    JobTemplate, 
    OfferTemplate, 
    TemplateExtraField
)
# Register your models here.

admin.site.register(JobApplicantTemplate)

admin.site.register(JobAssignmentTemplate)

admin.site.register(JobTemplate)

admin.site.register(OfferTemplate)

admin.site.register(TemplateExtraField)