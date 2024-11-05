import os
from django.http import HttpResponse
from django.core.files.storage import default_storage
from rest_framework import generics, exceptions
from rest_framework.viewsets import ModelViewSet
import markdown
from rest_framework.response import Response
from src.apps.applicant.tasks import send_offer_letter_email_task
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes, OpenApiParameter
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from src.apps.applicant.models import JobApplicant
from src.apps.common.utils import generate_pdf
from .models import (
    JobTemplate, 
    JobApplicantTemplate, 
    JobAssignmentTemplate, 
    OfferTemplate
   
)
from .serializers import (
    OfferLetterTemplateSerializer,
    JobAssignmentTemplateSerializer,
    JobApplicantTemplateSerializer,
    JobTemplateWriteSerializer,
    JobTemplateReadSerializer,
    OfferLetterRequestSerializer
)
from .filters import (
    OfferLetterFilterSet,
    JobAssignmentTemplateFilterSet,
    JobApplicantTemplateFilterSet,
    JobTemplateFilterSet
)


class OfferLetterTemplateViewSet(ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = OfferTemplate.objects.all()
    serializer_class = OfferLetterTemplateSerializer
    filterset_class = OfferLetterFilterSet

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        try:
            return OfferTemplate.objects.get(pk=pk)
        except OfferTemplate.DoesNotExist:
            raise exceptions.NotFound("Offer letter not found")
        
   
    


@extend_schema(
    request=OfferLetterRequestSerializer,
    responses={
        200: OpenApiTypes.BINARY,
        400: OpenApiTypes.OBJECT,
        500: OpenApiTypes.OBJECT
    },
    examples=[
        OpenApiExample(
            "Example request",
            description="Example of a request to send an offer letter.",
            value={
                "applicant_id": 1,
                "job_title": "Software Engineer",
                "department": "Engineering",
                "start_date": "2024-12-01",
                "supervisor": "John Doe",
                "location": "Remote",
                "base_salary": "100,000",
                "performance_bonus": "10,000",
                "acceptance_deadline": "2024-11-15",
                "representative_name": "Jane Smith",
                "contact_information": "info@mutaengine.com"
            },
            request_only=True
        )
    ],
    parameters=[
        OpenApiParameter(name="file", type=OpenApiTypes.BINARY, required=True, description="Markdown file for offer letter"),
        OpenApiParameter(name="html_template", type=OpenApiTypes.BINARY, required=False, description="HTML template file for offer letter"),
        OpenApiParameter(name="resume", type=OpenApiTypes.BINARY, required=False, description="Resume file")
    ],
    description="API to generate and send an offer letter as a PDF and email."
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def send_offer_letter(request):
    
    md_file = request.FILES.get('file')
        
    if not md_file:
        return Response({"error": "Markdown file required"}, status=400)

    
    content = md_file.read().decode('utf-8')
    
    appplicant_id = request.data.get('applicant_id')
    applicant=JobApplicant.objects.get(id=appplicant_id)
    applicant_name = f"{applicant.first_name} {applicant.last_name}"
    company_name = "Mutaengine"
    title = str(request.data.get('job_title', 'Position')),
    department = request.data.get('department', 'Department'),
    start_date = request.data.get('start_date', 'Start Date'),
    supervisor = request.data.get('supervisor', 'Supervisor'),
    location = request.data.get('location', 'Location'),
    base_salary = request.data.get('base_salary', 'Salary'),
    performance_bonus = request.data.get('performance_bonus', 'Bonus'),
    acceptance_deadline = request.data.get('acceptance_deadline', 'Deadline'),
    representative_name = request.data.get('representative_name', 'Representative'),
    to_email = str(applicant.email)
    placeholders = {
        "Candidate Name": applicant_name,
        "Job Title": request.data.get('job_title', 'Position'),
        "Company Name": request.data.get('company_name', 'Company'),
        "Department": request.data.get('department', 'Department'),
        "Start Date": request.data.get('start_date', 'Start Date'),
        "Supervisor": request.data.get('supervisor', 'Supervisor'),
        "Location": request.data.get('location', 'Location'),
        "Base Salary": request.data.get('base_salary', 'Salary'),
        "Performance Bonus": request.data.get('performance_bonus', 'Bonus'),
        "Acceptance Deadline": request.data.get('acceptance_deadline', 'Deadline'),
        "Company Representative's Name": request.data.get('representative_name', 'Representative'),
        "Company Contact Information": request.data.get('contact_information', 'Contact Info')
    }
    
    # Generate the PDF
    pdf_buffer = generate_pdf(content, placeholders)
    
    if not pdf_buffer:
        return Response({"error": "PDF generation failed"}, status=500)
    
    
    offer_letter_relative_path=None
    html_template_relative_path=None
    resume_relative_path=None
    html_file = request.FILES.get('html_template')
    resume_file = request.FILES.get('resume')

    
    if pdf_buffer:
        try:
            pdf_file_path = os.path.join('offer_letters', f"{applicant.first_name}_{applicant.last_name}_offer_letter.pdf")
            path = default_storage.save(pdf_file_path, pdf_buffer)
            offer_letter_relative_path = path
            print(f"Offer letter saved at: {offer_letter_relative_path}")
        except Exception as e:
            print(f"Error saving offer letter: {e}")
    
    if html_file:
        try:
            html_file_path = os.path.join('templates', html_file.name)
            path = default_storage.save(html_file_path, html_file)
            html_template_relative_path = path
            print(f"HTML template saved at: {html_template_relative_path}")
        except Exception as e:
            print(f"Error saving HTML template: {e}")
    
    if resume_file:
        try:
            resume_file_path = os.path.join('resumes', resume_file.name)
            path = default_storage.save(resume_file_path, resume_file)
            resume_relative_path = path
            print(f"Resume saved at: {resume_relative_path}")
        except Exception as e:
            print(f"Error saving resume: {e}")
    
    send_offer_letter_email_task.apply_async(
        str(company_name),
        str(applicant_name),
        str(appplicant_id),
        str(to_email),str(title),
        str(department),
        str(start_date),
        str(supervisor),
        str(location),
        str(base_salary),
        str(performance_bonus),kwargs={
        'resume_relative_path': resume_relative_path,
        'html_template_relative_path': html_template_relative_path,
        'offer_letter_relative_path': offer_letter_relative_path
       }, countdown=3)
    
    
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="offer_letter.pdf"'
    return response

    
    

class JobAssignmentTemplateViewSet(ModelViewSet):
    queryset = JobAssignmentTemplate.objects.all()
    serializer_class = JobAssignmentTemplateSerializer
    filterset_class = JobAssignmentTemplateFilterSet

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        try:
            return JobAssignmentTemplate.objects.get(pk=pk)
        except JobAssignmentTemplate.DoesNotExist:
            raise exceptions.NotFound("Job assignment template not found")
    
    

class JobApplicantTemplateViewSet(ModelViewSet):
    queryset = JobApplicantTemplate.objects.all()
    serializer_class = JobApplicantTemplateSerializer
    filterset_class = JobApplicantTemplateFilterSet

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        try:
            return JobApplicantTemplate.objects.get(pk=pk)
        except JobApplicantTemplate.DoesNotExist:
            raise exceptions.NotFound("Job applicant template not found")


class JobTemplateCreateView(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = JobTemplateWriteSerializer


class JobTemplateUpdateView(generics.UpdateAPIView):
    queryset = JobTemplate.objects.all()
    serializer_class = JobTemplateWriteSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
           return JobTemplate.objects.get(pk=pk)
        except JobTemplate.DoesNotExist:
            raise exceptions.NotFound("Job not found")
        

class JobTemplateListView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = JobTemplate.objects.all()
    serializer_class = JobTemplateReadSerializer
    filterset_class = JobTemplateFilterSet


class JobTemplateRetrieveView(generics.RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = JobTemplate.objects.all()
    serializer_class = JobTemplateReadSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
           return JobTemplate.objects.get(pk=pk)
        except JobTemplate.DoesNotExist:
            raise exceptions.NotFound("Job not found")

class JobTemplateDeleteView(generics.DestroyAPIView):
    queryset = JobTemplate.objects.all()
    serializer_class = JobTemplateReadSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
           return JobTemplate.objects.get(pk=pk)
        except JobTemplate.DoesNotExist:
            raise exceptions.NotFound("Job not found")
