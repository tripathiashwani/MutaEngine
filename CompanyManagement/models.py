from django.db import models
import uuid

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/')
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    linkedin = models.URLField(max_length=255)
    other_social_links = models.JSONField(blank=True, null=True)  # Can store additional social media links as JSON

    def __str__(self):
        return self.name
