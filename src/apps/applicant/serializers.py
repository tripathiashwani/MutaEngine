from rest_framework import serializers
from .tasks import send_assignment_email_task
import os
from django.core.files.storage import default_storage
from django.conf import settings
from .models import JobApplicant, JobApplicantExtraField, AssignmentSubmission

from src.apps.company.models import Company

class JobApplicantExtraFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplicantExtraField
        exclude = ["job_applicant","is_deleted"]




class JobApplicantSerializer(serializers.ModelSerializer):
    job_applicant_extra_fields = JobApplicantExtraFieldSerializer(many=True, required=False)

    class Meta:
        model = JobApplicant
        exclude = ["is_deleted"]

    def create(self, validated_data):
        extra_fields_data = validated_data.pop('job_applicant_extra_fields', [])

        job_applicant = JobApplicant.objects.create(**validated_data)

        
        if extra_fields_data:
            for extra_field_data in extra_fields_data:
                JobApplicantExtraField.objects.create(**extra_field_data, job_applicant=job_applicant)

        
        request = self.context['request']
        # company_name = Company.objects.all().first().name
        company_name="Mutaengine"
        applicant_name = f"{job_applicant.first_name} {job_applicant.last_name}"
        to_email = job_applicant.email
        role = str(job_applicant.job_template.title ) 
        last_date = job_applicant.job_template.deadline 
        assignment_detail_link = request.data.get('assignment_detail_link')
        application_id = str(job_applicant.id)
         # Initialize paths
        html_template_relative_path = None
        resume_relative_path = None

        # Save uploaded HTML template file
        html_file = request.FILES.get('html_template')
        print(request.FILES)
        if html_file:
            try:
                html_file_path = os.path.join('templates', html_file.name)
                path = default_storage.save(html_file_path, html_file)
                html_template_relative_path = path
                print(f"HTML template saved at: {html_template_relative_path}")
            except Exception as e:
                print(f"Error saving HTML template: {e}")


        # Save uploaded resume file
        resume_file = request.FILES.get('resume')
        if resume_file:
            try:
                resume_file_path = os.path.join('resumes', resume_file.name)
                path = default_storage.save(resume_file_path, resume_file)
                resume_relative_path = path
                print(f"Resume saved at: {resume_relative_path}")
            except Exception as e:
                print(f"Error saving resume: {e}")

        # Pass relative paths to the Celery task
        send_assignment_email_task.apply_async(
            (str(company_name), applicant_name, to_email, role, last_date, assignment_detail_link, application_id, resume_relative_path, html_template_relative_path),
            countdown=3
        )

        return job_applicant


class AssignmentSubmissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignmentSubmission
        exclude = ["is_deleted"]