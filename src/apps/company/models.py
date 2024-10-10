from django.db import models
from src.apps.common.models import BaseModel
from src.apps.common.utils import get_upload_folder
# Create your models here.

class Company(BaseModel):
    name = models.CharField(max_length=250, null=False, blank=False)
    address = models.CharField(max_length=250, null=True, blank=True)
    logo = models.ImageField(upload_to=get_upload_folder, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=17, null=True, blank=True)
    linkedin = models.URLField()

    def __str__(self):
        return self.name
