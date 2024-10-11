from celery import shared_task
from src.apps.mail.handlers import MailHandler


@shared_task
def send_otp_email_task(email: str, otp: str, action: str | None = None):
    mail_service_handler = MailHandler(smtp=None)
    mail_service_handler.send(
        subject=f"{str(action).capitalize()} OTP",
        text_body=otp,
        html_body=None,
        recepient_list=[email],
        fail_silently=True,
    )