from django.db import models
import uuid

class Mail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Name of the sender")
    username = models.EmailField(help_text="Email address of the sender")
    password = models.CharField(max_length=255, help_text="Encrypted password")
    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField()
    use_tls = models.BooleanField(default=False)
    use_ssl = models.BooleanField(default=False)
    system_default = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey('UserManagement.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
