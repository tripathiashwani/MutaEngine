from django.db import models
from src.apps.common.models import BaseModel
from src.apps.common.utils import get_upload_folder
# Create your models here.

from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"


class Company(BaseModel):
    name = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=True, blank=True)  
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ImageField(upload_to=get_upload_folder, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=17, null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    location = models.URLField(null=True, blank=True)  
    founded_date = models.DateField(null=True, blank=True)  
    industry = models.CharField(max_length=100, null=True, blank=True)  
    number_of_employees = models.IntegerField(null=True, blank=True)  
    website = models.URLField(null=True, blank=True)  
    facebook = models.URLField(null=True, blank=True)  
    twitter = models.URLField(null=True, blank=True)  
    instagram = models.URLField(null=True, blank=True)  

    def __str__(self):
        return self.name
