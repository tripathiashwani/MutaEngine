from celery import shared_task
from ..mailers.assignment_mailer import send_assignment
from ..mailers.confirmation_mailer import send_confirmation_email
from ..mailers.offer_letter_mailer import send_offer_letter
from ..mailers.otp_mailer import send_otp_mail
from ..mailers.password_credentials_mailer import password_credentials_mailer
from ..mailers.welcome_mailer import send_welcome_email

from django.utils import timezone
import os

# send_assignment(company_name, applicant, to_email, role, last_date, assignment_detail_link, application_id, resume_path=None, html_template_path=None)
@shared_task
def send_assignment_email_task(
    company_name, applicant, to_email, role, last_date, assignment_detail_link, application_id, resume_path=None, html_template_path=None
):
    print("Sending assignment email 2")
    # Pass the arguments to the email sending function
    send_assignment(
        company_name, 
        applicant, 
        to_email, 
        role, 
        last_date, 
        assignment_detail_link, 
        application_id, 
        resume_path if resume_path else None,  # Ensure it's passed as None if not present
        html_template_path if html_template_path else None  # Ensure it's passed as None if not present
    )


    
@shared_task
def send_confirmation_email_task(company_name, applicant, to_email, role, joining_date, manager, application_id, resume_path=None, html_template_path=None):
    send_confirmation_email(company_name, applicant, to_email, role, joining_date, manager, application_id, resume_path, html_template_path)

@shared_task
def send_offer_letter_task(company_name, applicant, to_email, role, offer_details, manager_name, offer_letter_path=None, html_template_path=None):
    send_offer_letter(company_name, applicant, to_email, role,offer_details, manager_name, offer_letter_path, html_template_path)

@shared_task
def send_otp_mail_task(employee_name, to_email, otp, company_name):
    send_otp_mail(employee_name, to_email, otp, company_name)

@shared_task
def password_credentials_mailer_task(employee_name, to_email, username, password,manager):
    password_credentials_mailer(employee_name, to_email, username, password,manager)

@shared_task
def send_welcome_email_task(company_name, new_employee, to_email, role, manager_name, welcome_message, html_template_path=None):
    send_welcome_email(company_name, new_employee, to_email, role, manager_name, welcome_message, html_template_path)





