from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet

from .serializers import JobApplicantSerializer, AssignmentSubmissionsSerializer
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