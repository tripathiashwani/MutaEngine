from django.db import models
import uuid

class TemplateExtraField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('textarea', 'Textarea'), ('checkbox', 'Checkbox'), ('radio', 'Radio'), ('select', 'Select'), ('rich_text', 'Rich Text')])
    required = models.BooleanField(default=False)
    options = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.label
