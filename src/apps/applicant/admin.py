from django.contrib import admin
from .models import JobApplicant, JobApplicantExtraField, AssignmentSubmission

# Register your models here.
admin.site.register(JobApplicant)

admin.site.register(JobApplicantExtraField)

admin.site.register(AssignmentSubmission)