from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet

from ..serializers.applicant_serializers import JobApplicantSerializer
from ..models.applicant import JobApplicant


class JobApplicantViewSet(ModelViewSet):
    serializer_class = JobApplicantSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return JobApplicant.objects.get(pk=pk)
        except JobApplicant.DoesNotExist:
            raise exceptions.NotFound("Job applicant not found")