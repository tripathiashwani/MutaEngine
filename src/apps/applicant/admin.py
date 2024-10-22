from django.contrib import admin
from .models import JobApplicant, JobApplicantExtraField

# Register your models here.
admin.site.register(JobApplicant)

admin.site.register(JobApplicantExtraField)