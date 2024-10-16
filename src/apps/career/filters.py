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


class JobApplicantTemplateFilterSet(BaseFilterSet):
    
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = JobApplicantTemplate
        fields = ("title",)


class JobTemplateFilterSet(BaseFilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    work_location = django_filters.CharFilter(field_name="work_location", lookup_expr="icontains")
    work_type = django_filters.CharFilter(field_name="work_type", lookup_expr="icontains")

    class Meta:
        model = JobTemplate
        fields = ("title",)