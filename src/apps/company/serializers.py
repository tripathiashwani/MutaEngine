from rest_framework import serializers

from .models import Company


class CompanySerailizer(serializers.ModelSerializer):

    class Meta:
        model = Company
        exclude = ["is_deleted"]