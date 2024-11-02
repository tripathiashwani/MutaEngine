from rest_framework import serializers

from .models import (
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


class JobTemplateWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = JobTemplate
        exclude = ["is_deleted"]


class JobTemplateReadSerializer(serializers.ModelSerializer):
    job_applicant_template = serializers.SerializerMethodField()
    job_assignment_template = serializers.SerializerMethodField()
    offer_template = serializers.SerializerMethodField()

    class Meta:
        model = JobTemplate
        exclude = ["is_deleted"]
    
    def get_job_applicant_template(self, obj):
        if obj.job_applicant_template:
            return JobApplicantTemplateSerializer(obj.job_applicant_template).data
        else:
            return None
        
    def get_job_assignment_template(self, obj):
        if obj.job_assignment_template:
            return JobAssignmentTemplateSerializer(obj.job_assignment_template).data
        else:
            return None
        
    def get_offer_template(self, obj):
        if obj.offer_template:
            return OfferLetterTemplateSerializer(obj.offer_template).data
        else:
            return None
        

class OfferLetterRequestSerializer(serializers.Serializer):
    applicant_id = serializers.IntegerField()
    job_title = serializers.CharField(required=False, default="Position")
    department = serializers.CharField(required=False, default="Department")
    start_date = serializers.CharField(required=False, default="Start Date")
    supervisor = serializers.CharField(required=False, default="Supervisor")
    location = serializers.CharField(required=False, default="Location")
    base_salary = serializers.CharField(required=False, default="Salary")
    performance_bonus = serializers.CharField(required=False, default="Bonus")
    acceptance_deadline = serializers.CharField(required=False, default="Deadline")
    representative_name = serializers.CharField(required=False, default="Representative")
    contact_information = serializers.CharField(required=False, default="Contact Info")
    file = serializers.FileField(required=True)
    html_template = serializers.FileField(required=False)
    resume = serializers.FileField(required=False)