import time

from decouple import config
from django.core.cache import cache
from django.utils import timezone
from django.utils.crypto import get_random_string

from src.apps.common.exceptions import InvalidRequest

from .models import User
from .tasks import send_otp_email_task


class OTPACTION:
    LOGIN = "login"
    RESET = "reset"
    VERIFY = "verify"


class TwoFAHandler:
    def __init__(
        self,
        user: User,
        resend_delay=int(config("OTP_RESEND_DELAY", cast=int, default=60)),  # type: ignore
        request_limit=int(config("OTP_REQUEST_LIMIT", cast=int, default=2)),  # type: ignore
        valid_period=int(config("OTP_VALID_PERIOD", cast=int, default=5)),  # type: ignore
        action=None,
    ) -> None:
        self.user = user
        self.resend_delay = resend_delay
        self.last_resend_time = cache.get(f"last_resend_time_{self.user.id}", None)
        self.request_limit = request_limit
        self.valid_period = valid_period
        self.action = action

    def assign_otp(self):
        if cache.get(f"resend_count_{self.user.id}_{self.action}", 0) >= self.request_limit:
            raise InvalidRequest("Too many attempt. Please try again later.")

        if (
            self.last_resend_time
            and time.time() - float(self.last_resend_time) < self.resend_delay
        ):
            raise InvalidRequest("You can't resend otp now. Please try again later.")

        otp = get_random_string(length=6, allowed_chars="0123456789")
        self.user.otp = otp
        self.user.otp_created_at = timezone.now()
        self.user.save()

        cache.set(f"last_resend_time_{self.user.id}_{self.action}", time.time(), timeout=180)
        last_resend_count = cache.get(f"resend_count_{self.user.id}_{self.action}", 0)
        cache.set(f"resend_count_{self.user.id}_{self.action}", last_resend_count + 1, timeout=180)

        return otp

    def verify_otp(self, otp: str):
        if self.user.otp != otp:
            return False, "Invalid OTP"

        if (
            self.user.otp_created_at
            and self.user.otp_created_at + timezone.timedelta(minutes=self.valid_period)
            < timezone.now()
        ):
            return False, "OTP expired"

        self.user.otp = None
        self.user.otp_created_at = None
        self.user.save()

        return True, "OTP verified"

    def send_otp(
        self,
    ):
        self.assign_otp()

        send_otp_email_task.delay(email=self.user.email, action=self.action, otp=self.user.otp)

        message = "OTP sent successfully via email"
        return message
