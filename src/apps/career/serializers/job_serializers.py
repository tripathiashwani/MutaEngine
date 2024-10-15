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
        exclude = ["is_deleted"]


class JobAssignmentTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobAssignmentTemplate
        exclude = ["is_deleted"]


class TemplateExtraFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateExtraField
        exclude = ["is_deleted"]

class JobApplicantTemplateSerializer(serializers.ModelSerializer):
    template_extra_fields = TemplateExtraFieldSerializer(many=True)

    class Meta:
        model = JobApplicantTemplate
        exclude = ["is_deleted"]

    def create(self, validated_data):
        template_extra_fields = validated_data.pop('template_extra_fields')
        job_applicant_template = JobApplicantTemplate.objects.create(**validated_data)
        
        for template_extra_field in template_extra_fields:
            extra_fields = TemplateExtraField.objects.create(**template_extra_field)
            job_applicant_template.template_extra_fields.add(extra_fields)

        return job_applicant_template