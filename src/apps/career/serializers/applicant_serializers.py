from rest_framework import serializers

from ..models.applicant import JobApplicant, JobApplicantExtraField

class JobApplicantExtraFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplicantExtraField
        exclude = ["job_applicant","is_deleted"]


class JobApplicantSerializer(serializers.ModelSerializer):
    job_applicant_extra_fields = JobApplicantExtraFieldSerializer(many=True, required=False)

    class Meta:
        model = JobApplicant
        exclude = ["is_deleted"]

    def create(self, validated_data):
        extra_fields_data = validated_data.pop('job_applicant_extra_fields', [])
        job_applicant = JobApplicant.objects.create(**validated_data)

        if extra_fields_data:
            for extra_field_data in extra_fields_data:
                extra_field = JobApplicantExtraField.objects.create(**extra_field_data, job_applicant=job_applicant)
        
        return super().create(validated_data)
