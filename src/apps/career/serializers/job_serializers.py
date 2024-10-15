from rest_framework import serializers

from ..models.job import (
    JobTemplate, 
    JobApplicantTemplate, 
    JobAssignmentTemplate, 
    TemplateExtraField,
    OfferTemplate
)


class OfferLetterTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferTemplate
        fields = '__all__'


class JobAssignmentTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobAssignmentTemplate
        fields = '__all__'