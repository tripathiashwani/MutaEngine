from rest_framework import serializers
from .tasks import send_assignment_email  
import os
from django.core.files.storage import default_storage
from django.conf import settings
from .models import JobApplicant, JobApplicantExtraField, AssignmentSubmission

from company.models import Company

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
        company_name = Company.name
        applicant_name = f"{job_applicant.first_name} {job_applicant.last_name}"
        to_email = job_applicant.email
        role = job_applicant.job_template.title  
        last_date = job_applicant.job_template.deadline 
        assignment_detail_link = request.data.get('assignment_detail_link')
        application_id = job_applicant.id
        resume_path = None  

        html_template_path = None
        
        html_file = request.FILES.get('html_template')
        resume_file=request.FILES.get('resume')

        if html_file:
           
            html_file_path = os.path.join(settings.MEDIA_ROOT, 'templates', html_file.name)
            path = default_storage.save(html_file_path, html_file)
            html_template_path = os.path.join(settings.MEDIA_ROOT, path)
        
        if resume_file:
            
            resume_file_path = os.path.join(settings.MEDIA_ROOT, 'resumes', resume_file.name)
            path = default_storage.save(resume_file_path, resume_file)
            resume_path = os.path.join(settings.MEDIA_ROOT, path)

       
        send_assignment_email.apply_async((company_name, applicant_name, to_email, role, last_date, assignment_detail_link, application_id, resume_path, html_template_path), countdown=12*3600)


        return job_applicant


class AssignmentSubmissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignmentSubmission
        exclude = ["is_deleted",]

    def create(self, validated_data):
        appicant_id = validated_data.get('applicant_id')
        try:
            applicant = JobApplicant.objects.get(id=appicant_id)
        except JobApplicant.DoesNotExist:
            raise serializers.ValidationError("Job applicant not found")

        assignment_submitted = AssignmentSubmission.objects.create(**validated_data)

        applicant.assignment_submitted = True
        applicant.save()

        return assignment_submitted

class OfferletterSubmission(serializers.ModelSerializer):

    class Meta:
        model = JobApplicant
        fields = ['id', 'signed_offer_letter']
