from rest_framework import generics
from rest_framework.viewsets import ModelViewSet


from ..models.job import (
    JobTemplate, 
    JobApplicantTemplate, 
    JobAssignmentTemplate, 
    OfferTemplate
)
from ..serializers.job_serializers import (
    OfferLetterTemplateSerializer,
    JobAssignmentTemplateSerializer,
    JobApplicantTemplateSerializer,
)
from ..filters import (
    OfferLetterFilterSet,
    JobAssignmentTemplateFilterSet,
    JobApplicantTemplateFilterSet,
)


class OfferLetterTemplateViewSet(ModelViewSet):
    queryset = OfferTemplate.objects.all()
    serializer_class = OfferLetterTemplateSerializer
    filterset_class = OfferLetterFilterSet


class JobAssignmentTemplateViewSet(ModelViewSet):
    queryset = JobAssignmentTemplate.objects.all()
    serializer_class = JobAssignmentTemplateSerializer
    filterset_class = JobAssignmentTemplateFilterSet


class JobApplicantTemplateViewSet(ModelViewSet):
    queryset = JobApplicantTemplate.objects.all()
    serializer_class = JobApplicantTemplateSerializer
    filterset_class = JobApplicantTemplateFilterSet
