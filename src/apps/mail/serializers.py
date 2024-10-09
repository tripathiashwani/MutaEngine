from rest_framework import serializers

from .models import SMTP


class SMTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = SMTP
        fields = "__all__"