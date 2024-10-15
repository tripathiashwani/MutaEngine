import django_filters

from src.apps.common.filters import BaseFilterSet

from .models.job import (
    JobTemplate, 
    JobApplicantTemplate, 
    JobAssignmentTemplate, 
    OfferTemplate
)


class OfferLetterFilterSet(BaseFilterSet):
    
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = OfferTemplate
        fields = ("title",)


class JobAssignmentTemplateFilterSet(BaseFilterSet):
    
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = JobAssignmentTemplate
        fields = ("title",)