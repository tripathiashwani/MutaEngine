from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from .serializers import JobApplicantSerializer, AssignmentSubmissionsSerializer, OfferletterSubmissionSerializer
from .models import JobApplicant, AssignmentSubmission

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

        return Response(serializer.data, status=status.HTTP_200_OK)
