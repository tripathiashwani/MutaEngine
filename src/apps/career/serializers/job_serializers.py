from rest_framework import serializers

from ..models.job import JobTemplate, JobApplicantTemplate, JobAssignmentTemplate, OfferTemplate


class OfferLetterTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferTemplate
        fields = '__all__'


