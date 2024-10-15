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


class TemplateExtraFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateExtraField
        fields = '__all__'

class JobApplicantTemplateSerializer(serializers.ModelSerializer):
    template_extra_fields = TemplateExtraFieldSerializer(many=True)

    class Meta:
        model = JobApplicantTemplate
        fields = '__all__'

    def create(self, validated_data):
        template_extra_fields = validated_data.pop('template_extra_fields')
        
        if template_extra_fields:
            template_extra_fields = TemplateExtraField.objects.bulk_create(template_extra_fields)

        job_applicant_template = JobApplicantTemplate.objects.create(**validated_data)
        job_applicant_template.template_extra_fields.set(template_extra_fields)

        return job_applicant_template