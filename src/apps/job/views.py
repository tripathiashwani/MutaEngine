from rest_framework import generics, exceptions
from rest_framework.viewsets import ModelViewSet


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
)
from .filters import (
    OfferLetterFilterSet,
    JobAssignmentTemplateFilterSet,
    JobApplicantTemplateFilterSet,
    JobTemplateFilterSet,
)


class OfferLetterTemplateViewSet(ModelViewSet):
    queryset = OfferTemplate.objects.all()
    serializer_class = OfferLetterTemplateSerializer
    filterset_class = OfferLetterFilterSet

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        try:
            return OfferTemplate.objects.get(pk=pk)
        except OfferTemplate.DoesNotExist:
            raise exceptions.NotFound("Offer letter not found")

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
