from rest_framework import serializers
from .tasks import send_assignment_email_task , send_offer_letter_email_task, send_mail_task
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.template.loader import render_to_string
from .models import JobApplicant, JobApplicantExtraField, AssignmentSubmission
from src.apps.common.checks import is_safe_pdf
from src.apps.company.models import Company
from src.apps.common.utils import generate_pdf
from uuid import UUID

class JobApplicantExtraFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplicantExtraField
        exclude = ["job_applicant"]


class JobApplicantSerializer(serializers.ModelSerializer):
    job_applicant_extra_fields = JobApplicantExtraFieldSerializer(many=True, required=False)

    class Meta:
        model = JobApplicant
        fields = "__all__"

    def create(self, validated_data):
        extra_fields_data = validated_data.pop('job_applicant_extra_fields', [])

        job_template = validated_data.get("job_template",None)

        if job_template is None:
            raise serializers.ValidationError("Job template is required")
        
        job_deadline = job_template.deadline

        from django.utils import timezone
        current_date = timezone.now()
        if job_deadline < current_date:
            raise serializers.ValidationError("Application cannot be submiited: passed deadline")

        request = self.context['request']
        resume_file = request.FILES.get('resume')
        if resume_file:
            if not is_safe_pdf(resume_file):
                raise serializers.ValidationError("Invalid resume file format. Only PDF files are allowed.")

        job_applicant = JobApplicant.objects.create(**validated_data)

        
        if extra_fields_data:
            for extra_field_data in extra_fields_data:
                JobApplicantExtraField.objects.create(**extra_field_data, job_applicant=job_applicant)

        company : Company = Company.objects.all().first() # type: ignore
        objective = job_applicant.job_template.job_assignment_template.objective # type: ignore

        subject = f"Assignment for {job_applicant.job_template.title} at {company.name}"
        text_body = None
        html_body = render_to_string(
            'application.html', 
            {
                'company': company.name,
                'applicant': job_applicant,
                'objective': objective,
            }
        )
        recepient_list = [job_applicant.email]
        # attachments = None

        send_mail_task.apply_async(
            args=[subject, text_body, html_body, recepient_list, None, company.name],
            countdown=3,
        )

        # company_name = Company.objects.all().first().name
        # company_name="Mutaengine"
        # applicant_name = f"{job_applicant.first_name} {job_applicant.last_name}"
        # to_email = job_applicant.email
        # role = str(job_applicant.job_template.title ) 
        # last_date = job_applicant.job_template.deadline 
        # # assignment_detail_link = f"https://career.mutaengine.cloud/career/{job_applicant.job_template.pk}/submit-assignment-form"
        # # assignment_detail_link = f"https://career.mutaengine.cloud/career/{job_applicant.job_template.job_assignment_template.id}/assignment-details"
        # assignment_detail_link = f"https://career.mutaengine.cloud/career/{job_applicant.job_template.id}/assignment-details"
        # assignment_detail=request.data.get('assignment_detail')
        # application_id = str(job_applicant.application_id)
        #  # Initialize paths
        # html_template_relative_path = None
        # resume_relative_path = None
        # assignment_objective=job_applicant.job_template.job_assignment_template.objective

        # Save uploaded HTML template file
        html_file = request.FILES.get('html_template')
        # print(request.FILES)
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
        # resume_file=None
        if resume_file:
            try:
                resume_file_path = os.path.join('resumes', resume_file.name)
                path = default_storage.save(resume_file_path, resume_file)
                
                
                resume_relative_path = None
                print(f"Resume saved at: {resume_relative_path}")
            except Exception as e:
                print(f"Error saving resume: {e}")

        # # Pass relative paths to the Celery task
        # send_assignment_email_task.apply_async(
        #     (str(company_name), applicant_name, to_email, role, last_date, assignment_detail_link, assignment_detail, application_id,assignment_objective),
        #     countdown=3,
        #     kwargs={
        #         'resume_relative_path': resume_relative_path,
        #         'html_template_relative_path': html_template_relative_path
        #     }
        # )
        job_applicant.assignment_sent=True
        job_applicant.save()
        return job_applicant


class AssignmentSubmissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignmentSubmission
        fields = "__all__"

    def create(self, validated_data):

        applicant_id=validated_data.get('applicant_id')
        
        try:
            application=JobApplicant.objects.get(application_id=applicant_id)
        except JobApplicant.DoesNotExist:
            raise serializers.ValidationError("Application not found")
        
        job_deadline = application.job_template.deadline

        from django.utils import timezone
        current_date = timezone.now()

        if job_deadline < current_date:
            raise serializers.ValidationError("Assignment cannot be submiited: passed deadline")

        
        assignment_submission = AssignmentSubmission.objects.create(**validated_data)

        company = Company.objects.all()
        if company:
            company_name=company.first().name # type: ignore
        else:
            company_name="Mutaengine"
        
        application.assignment_submitted=True
        role=str(application.job_template.title)
        applicant_name = f"{application.first_name} {application.last_name}"
        to_email = str(application.email)
        html_template_relative_path = None
        resume_relative_path = None
        offer_letter_relative_path = None
        request = self.context['request']
        offer_details = request.data.get('offer_details')
        manager_name = request.data.get('manager_name')
        performance_bonus = request.data.get('performance_bonus')
        base_salary = request.data.get('base_salary')

        # Save uploaded HTML template file
        # html_file = request.FILES.get('html_template')
        # print(request.FILES)
        # if html_file:
        #     try:
        #         html_file_path = os.path.join('templates', html_file.name)
        #         path = default_storage.save(html_file_path, html_file)
        #         html_template_relative_path = path
        #         print(f"HTML template saved at: {html_template_relative_path}")
        #     except Exception as e:
        #         print(f"Error saving HTML template: {e}")


        # # Save uploaded resume file
        # resume_file = request.FILES.get('resume')
        # if resume_file:
        #     try:
        #         resume_file_path = os.path.join('resumes', resume_file.name)
        #         path = default_storage.save(resume_file_path, resume_file)
        #         resume_relative_path = path
        #         print(f"Resume saved at: {resume_relative_path}")
        #     except Exception as e:
        #         print(f"Error saving resume: {e}")

        # offer_letter_file_html = request.FILES.get('offer_letter_html')

        offer_letter_file_html = (
            application.job_template.offer_template.html_content 
            if application.job_template.offer_template is not None and application.job_template.offer_template.html_content is not None
            else render_to_string("default_offer_letter.html")
        )
        
        
        application.save()
    #    def send_offer_letter_email_task(company_name, applicant, applicant_id,to_email, title,department,start_date , supervisor,location,base_salary,performance_bonus, resume_relative_path=None, offer_letter_relative_path=None, html_template_relative_path=None):
        send_offer_letter_email_task.apply_async(
            (
                company_name, applicant_name, applicant_id, to_email, role, application.job_template.title, application.joining_date,
                manager_name, application.job_template.work_location,application.job_template.id, base_salary, performance_bonus,
                resume_relative_path, html_template_relative_path, offer_letter_file_html
            ),
            countdown=3
        )
        return assignment_submission
    
class OfferletterSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplicant
        fields = ['application_id', 'submitted_offer_letter']

    def validate(self, attrs):
        if not attrs.get('application_id'):
            raise serializers.ValidationError('Job application ID is required')

        if not attrs.get('submitted_offer_letter'):
            raise serializers.ValidationError('Signed Offer letter is required')
        
        return super().validate(attrs)

def get_pdf(file, applicant_id):
    try:
        # Read the HTML content of the uploaded file
        # Check if 'file' is already a string (HTML content)
        if isinstance(file, str):
            html_content = file
        else:
            # Otherwise, assume it's a file-like object and read its content
            html_content = file.read().decode('utf-8')  # Assuming UTF-8 encoding

        # Validate and retrieve applicant information
        # applicant_id = request.data.get('applicant_id')
        try:
            # applicant_id = UUID(applicant_id)  # Attempt to convert to UUID
            applicant = JobApplicant.objects.get(application_id=applicant_id)
        except (ValueError, TypeError):
            print(f"Invalid UUID for applicant_id: {applicant_id}")
            return None
        except JobApplicant.DoesNotExist:
            print("Applicant not found.")
            return None
        
        applicant_name = f"{applicant.first_name} {applicant.last_name}"
        
        company = Company.objects.all()
        if company:
            company_name=company.first().name # type: ignore
        else:
            company_name="Mutaengine"

        # Get other data from the request
        placeholders = {
            "Candidate Name": applicant_name,
            "Job Title": applicant.job_template.title,
            "Company Name": company_name,
            "Department": applicant.job_template.department,
            "Start Date": applicant.job_template.joining_date, # type: ignore
            "Supervisor": f"{applicant.manager.first_name} {applicant.manager.last_name}", # type: ignore
            "Location": "request.data.get('location', 'Location')",
            "Base Salary": "request.data.get('base_salary', 'Salary')",
            "Performance Bonus": "request.data.get('performance_bonus', 'Bonus')",
            "Acceptance Deadline": applicant.job_template.deadline,
            "Company Representative's Name": "request.data.get('representative_name', 'Representative')",
            "Company Contact Information": "request.data.get('contact_information', 'Contact Info')"
        }
    
        # Generate the PDF from the HTML content
        pdf_buffer = generate_pdf(html_content, placeholders)
        
        return pdf_buffer
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
    
class TilesDataSerializer(serializers.Serializer):
    active_job_post = serializers.IntegerField()
    new_job_applicant = serializers.IntegerField()
    assignment_to_review = serializers.IntegerField()