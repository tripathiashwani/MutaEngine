from django.db import models

from src.apps.common.models import BaseModel
from src.apps.auth.models import UserModelMixin
from src.apps.common.hashers import decrypt_password, encrypt_password


class SMTP(BaseModel,UserModelMixin):
    from_name = models.CharField(
        max_length=250, null=False, blank=False, help_text="Name of the sender"
    )

    host = models.CharField(max_length=250, null=False, blank=False)
    port = models.PositiveIntegerField(null=False, blank=False)

    username = models.CharField(
        max_length=250, null=False, blank=False, help_text="Email address of the sender"
    )
    password = models.CharField(max_length=250, null=False, blank=False)

    use_tls = models.BooleanField(default=False)
    use_ssl = models.BooleanField(default=False)

    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.from_name

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.password = encrypt_password(self.password)
        super(SMTP, self).save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = encrypt_password(raw_password)

    def get_password(self):
        return decrypt_password(self.password)

    def check_password(self, raw_password):
        return self.get_password() == raw_password
