from rest_framework import serializers

from .models import SMTP


class SMTPSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SMTP
        fields = "__all__"