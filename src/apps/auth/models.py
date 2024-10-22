from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


from src.apps.common.models import BaseModel, Status
from src.apps.common.utils import get_upload_folder, image_validate


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must have is_superuser=True")
        
        domain = email.split('@')[-1]  
        if domain != "mutaengine.cloud":
         raise ValueError("Superuser email must be from the 'mutaengine.cloud' domain.")

        return self.create_user(email, password, **extra_fields)


class User(BaseModel, AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=17, null=False, blank=False)
    image = models.ImageField(
        upload_to=get_upload_folder, validators=[image_validate], null=True, blank=True
    )
    address = models.CharField(max_length=250, null=True, blank=True)

    email_verified = models.BooleanField(default=False)
    enable_2fa = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    otp_tries = models.IntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]

    objects: CustomUserManager = CustomUserManager()

    def __str__(self) -> str:
        return self.email

class UserModelMixin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        abstract = True

class Role(Group):
    title = models.CharField(max_length=255, null=False, blank=False, unique=True)
    status = models.CharField(
        max_length=255, blank=False, null=False, choices=Status.choices, default=Status.ACTIVE
    )
    responsibilities = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    parent_role = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name='roles_created', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='roles_updated', on_delete=models.SET_NULL)


    def __str__(self):
        return self.name
