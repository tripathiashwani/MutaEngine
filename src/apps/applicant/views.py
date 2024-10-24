import os
from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from .serializers import JobApplicantSerializer, AssignmentSubmissionsSerializer, OfferletterSubmissionSerializer
from .models import JobApplicant, AssignmentSubmission
from src.apps.company.models import Company
from .tasks import send_confirmation_email_task
from django.core.files.storage import default_storage

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
        job_applicant_id = serializer.validated_data.get("id", None)

        try:
            job_applicant = JobApplicant.objects.get(id=job_applicant_id)
            job_applicant.offer_letter_signed = True
        except JobApplicant.DoesNotExist:
            raise exceptions.NotFound("Job applicant not found")
        
        job_applicant.submitted_offer_letter = serializer.validated_data.get("submitted_offer_letter",None)
        job_applicant.save()
        handle_mailer_task(request, job_applicant)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


def handle_mailer_task(request, applicant):
    company_name=str(Company.objects.all().first().name)
    applicant_name = f"{applicant.first_name} {applicant.last_name}"
    to_email = str(applicant.email)
    role = str(applicant.job_template.title)
    manager_name = str(applicant.manager_name)
    joining_date = str(applicant.joining_date)
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
        html_template_relative_path = None
        resume_relative_path = None
        offer_letter_relative_path = None
        
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
    class DummyRequest:
        FILES = {
            'html_template': open('dummy_template.html', 'rb'),
            'resume': open('dummy_resume.pdf', 'rb')
        }

    
  