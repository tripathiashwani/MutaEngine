from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection

from src.apps.mail.models import SMTP
from src.settings import DEFAULT_FROM_EMAIL


class MailHandler:
    def __init__(self, smtp: SMTP | None = None):
        self.smtp = smtp

    def get_default_connection_params(self):
        return {
            "host": settings.EMAIL_HOST,
            "port": settings.EMAIL_PORT,
            "use_tls": settings.EMAIL_USE_TLS,
            "user": settings.EMAIL_HOST_USER,
            "password": settings.EMAIL_HOST_PASSWORD,
            "from_name": settings.DEFAULT_FROM_EMAIL,
        }

    def _get_connection_params(self):
        if not self.smtp:
            return self.get_default_connection_params()
        return {
            "host": self.smtp.host,
            "port": self.smtp.port,
            "use_tls": self.smtp.use_tls,
            "user": self.smtp.username,
            "password": self.smtp.get_password(),
            "from_name": f"{self.smtp.from_name} <{self.smtp.username}>",
        }

    def send(
        self,
        subject: str,
        text_body: str,
        html_body: str | None,
        recepient_list: list[str],
        fail_silently=False,
        attachments: list | None = None,
    ):
        connection_params = self._get_connection_params()

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            to=recepient_list,
        )

        if html_body and html_body != "":
            email.content_subtype = "html"
            email.attach_alternative(html_body, "text/html")

        from_name = connection_params.pop("name", None)
        if connection_params:
            email.connection = get_connection(
                **connection_params, fail_silently=fail_silently
            )
            email.from_email = f"{from_name} < {connection_params['username']}>"
        else:
            email.from_email = DEFAULT_FROM_EMAIL

        if attachments:
            for attachment in attachments:
                email.attach_file(attachment)

        try:
            email.send()
            return "Email sent successfully", None
        except Exception as err:
            return "Error sending email", str(err)
