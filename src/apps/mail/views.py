from rest_framework.viewsets import ModelViewSet

from .serializers import SMTPSerializer
from .models import SMTP


class SMTPViewSet(ModelViewSet):
    queryset = SMTP.objects.all()
    serializer_class = SMTPSerializer