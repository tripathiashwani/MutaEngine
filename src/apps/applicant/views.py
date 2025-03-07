import os
from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from drf_spectacular.utils import extend_schema

from .serializers import (
    JobApplicantSerializer, 
    AssignmentSubmissionsSerializer, 
    OfferletterSubmissionSerializer,
    TilesDataSerializer,
    TemplateTestSerializer
)
from .models import JobApplicant, AssignmentSubmission
from src.apps.company.models import Company
from .tasks import send_confirmation_email_task, send_mail_task
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from src.apps.job.models import JobTemplate
from src.apps.mail.handlers import MailHandler

class JobApplicantViewSet(ModelViewSet):
    permission_classes = []
    authentication_classes = []
    serializer_class = JobApplicantSerializer

    def get_queryset(self):
        return JobApplicant.objects.filter(is_deleted=False)
    
    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return JobApplicant.objects.get(pk=pk)
        except JobApplicant.DoesNotExist:
            raise exceptions.NotFound("Job applicant not found")
        

class AssignmentSubmissionViewSet(ModelViewSet):
    permission_classes = []
    authentication_classes = []
    
    serializer_class = AssignmentSubmissionsSerializer
    
    def get_object(self):
        pk = self.kwargs.get("pk")
        # print(pk)
        try:
            return AssignmentSubmission.objects.get(pk=pk)
        except AssignmentSubmission.DoesNotExist:
            raise exceptions.NotFound("Assignment submission not found")
        
    def get_queryset(self):
        return AssignmentSubmission.objects.filter(is_deleted=False)
    

class SubmitSignedOfferLetterView(generics.GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = OfferletterSubmissionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        application_id = serializer.validated_data.get("application_id", None)

        try:
            job_applicant = JobApplicant.objects.get(application_id=application_id)
            job_applicant.offer_letter_signed = True
        except JobApplicant.DoesNotExist:
            raise exceptions.NotFound("Job applicant not found")
        
        job_applicant.submitted_offer_letter = serializer.validated_data.get("submitted_offer_letter",None)
        job_applicant.save()

        company : Company = Company.objects.all().first() # type: ignore

        subject = f"Offer Acceptance Confirmation for {job_applicant.job_template.title} at {company.name}"
        text_body = None
        html_body = render_to_string('offer_letter_recieved.html', {'company':company, 'applicant': job_applicant})
        recepient_list = [job_applicant.email]

        send_mail_task.apply_async(
            args=[subject, text_body, html_body, recepient_list, None, company.name],
            countdown=3,
        )

        subject = f"Offer Acceptance Confirmation for {job_applicant.job_template.title} at {company.name}"
        text_body = None
        html_body = render_to_string('welcome.html', {'company':company, 'applicant': job_applicant})


        send_mail_task.apply_async(
            args=[subject, text_body, html_body, recepient_list, None, company.name],
            countdown=15,
        )

        # handle_mailer_task(request, job_applicant)
        
        return Response({"msg":"Submitted successfully"}, status=status.HTTP_200_OK)


def handle_mailer_task(request, applicant):
    company_name="Mutaengine"
    applicant_name = f"{applicant.first_name} {applicant.last_name}"
    to_email = str(applicant.email)
    role = str(applicant.job_template.title)
    manager_name = str(applicant.manager.first_name) if applicant.manager else "Mutaengine"

    joining_date = str(applicant.joining_date)
    html_file = request.FILES.get('html_template')
    html_template_relative_path = None
    resume_relative_path = None
    offer_letter_relative_path = None
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
                
        
    send_confirmation_email_task.apply_async(
        (company_name,applicant_name,to_email,role,joining_date,manager_name,resume_relative_path,html_template_relative_path ),countdown=3
    )
    # (company_name, applicant, to_email, role, joining_date, manager_name, resume_path=resume_path, html_template_path=html_template_path)/

    return True

    # Dummy request and applicant data for testing handle_mailer_task
    

    
class TilesDataView(generics.GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = TilesDataSerializer

    def get(self, request, *args, **kwargs):

        active_job_post = JobTemplate.objects.only("id","status").filter(status="active").count()

        from django.utils import timezone
        from datetime import timedelta

        current_date = timezone.now()
        start_of_day = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        new_job_applicant = JobApplicant.objects.only("id","created_at").filter(
            created_at__gte=start_of_day,
            created_at__lt=end_of_day
        ).count()

        assignment_to_review = (
            AssignmentSubmission.objects
            .only("id","assignment_reviewed")
            .filter(assignment_reviewed=False).count()
        )

        data = {
            "active_job_post" : active_job_post,
            "new_job_applicant" : new_job_applicant,
            "assignment_to_review" : assignment_to_review,
        }

        serializer = self.get_serializer(data)

        return Response(serializer.data)

class TemplateTestView(generics.GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = TemplateTestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        recipient_email = serializer.validated_data.get("reciever_email")
        template = serializer.validated_data.get("template")

        # Check if template is an uploaded file
        if isinstance(template, InMemoryUploadedFile):
            # Read and decode the file content (assuming it's in utf-8)
            template_content = template.read().decode('utf-8')

            # Create a Template object using the file content
            template_obj = Template(template_content)

            # Define the context for rendering the template (empty for now)
            context = {}
            html_body = template_obj.render(Context(context))
        else:
            # Handle case where no template is provided
            return Response({"error": "Invalid template"}, status=status.HTTP_400_BAD_REQUEST)

        
        mail_handler = MailHandler(smtp=None)
        mail_handler.send(
            subject="Test Email",
            text_body="This is a test email",
            html_body=html_body,
            recepient_list=[recipient_email],
        )

        return Response({"msg":"Mail sent successfully"},status=status.HTTP_200_OK)
