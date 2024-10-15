from rest_framework import generics
from rest_framework.viewsets import ModelViewSet


from ..models.job import OfferTemplate
from ..serializers.job_serializers import OfferLetterTemplateSerializer
from ..filters import OfferLetterFilterSet


class OfferLetterTemplateViewSet(ModelViewSet):
    queryset = OfferTemplate.objects.all()
    serializer_class = OfferLetterTemplateSerializer
    filterset_class = OfferLetterFilterSet