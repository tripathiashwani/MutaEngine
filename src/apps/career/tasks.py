from celery import shared_task
from ..mailers.assignment_mailer import send_assignment  # import the mailer function
from django.utils import timezone
import os

@shared_task
def send_assignment_email(company_name, applicant, to_email, role, last_date, assignment_detail_link, application_id, resume_path=None, html_template_path=None):
    send_assignment(company_name, applicant, to_email, role, last_date, assignment_detail_link, application_id, resume_path, html_template_path)
