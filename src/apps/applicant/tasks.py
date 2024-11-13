from celery import shared_task
from src import settings
from src.apps.mail.mailers.assignment_mailer import send_assignment 
from src.apps.mail.mailers.confirmation_mailer import send_confirmation_email
from src.apps.mail.mailers.otp_mailer import send_otp_mail
from src.apps.mail.mailers.password_credentials_mailer import password_credentials_mailer
from src.apps.mail.mailers.welcome_mailer import send_welcome_email
from src.apps.mail.mailers.offer_letter_mailer import send_offer_letter
from src.apps.mail.handlers import MailHandler
from django.utils import timezone
import os
from django.core.files.storage import default_storage

@shared_task
def send_mail_task(subject, text_body, html_body, recepient_list, attachments, form_name):
    mail_handler = MailHandler()
    mail_handler.send(subject, text_body, html_body, recepient_list, attachments, form_name)
    print("mail sent")


# send_assignment(company_name, applicant, to_email, role, last_date, assignment_detail_link, application_id, resume_path=None, html_template_path=None)
@shared_task
def send_assignment_email_task(
    company_name, applicant, to_email, role, last_date, assignment_detail_link,assignment_detail, application_id,assignment_objective, resume_relative_path=None, html_template_relative_path=None
):
    
    resume_path = os.path.join(settings.MEDIA_ROOT, resume_relative_path) if resume_relative_path else None
    html_template_path = os.path.join(settings.MEDIA_ROOT, html_template_relative_path) if html_template_relative_path else None

    
    send_assignment(
        company_name, 
        applicant, 
        to_email, 
        role, 
        last_date, 
        assignment_detail_link, 
        assignment_detail,
        application_id, 
        assignment_objective,
        resume_path=resume_path, 
        html_template_path=html_template_path
    )

@shared_task
def send_offer_letter_email_task(
    company_name, company_logo, comapny_linkedin_url,applicant, applicant_id, to_email, title, department, start_date, 
    supervisor, location,job_template_id, base_salary, performance_bonus, 
    resume_relative_path, html_template_relative_path, offer_letter_file_html
):
    from .serializers import get_pdf
    
    offer_letter_file = get_pdf(offer_letter_file_html,applicant_id)

    print(offer_letter_file,"offer letter file")

    if offer_letter_file:
        try:
            offer_letter_file_path = os.path.join('offer_letters', f"{applicant}_offer_letter.pdf")
            path = default_storage.save(offer_letter_file_path,offer_letter_file)
            offer_letter_relative_path = path
            print(f"offer_letter saved at: {offer_letter_relative_path}")
        except Exception as e:
            print(f"Error saving offer_letter: {e}")

    offer_letter_path = os.path.join(settings.MEDIA_ROOT, offer_letter_relative_path) if offer_letter_relative_path else None
    html_template_path = os.path.join(settings.MEDIA_ROOT, html_template_relative_path) if html_template_relative_path else None
    resume_path = os.path.join(settings.MEDIA_ROOT, resume_relative_path) if resume_relative_path else None
    send_offer_letter(
        company_name, company_logo, comapny_linkedin_url,applicant, applicant_id, to_email, title, department, start_date, 
        supervisor, location,job_template_id, base_salary, performance_bonus, 
        resume_path=resume_path, offer_letter_path=offer_letter_path, html_template_path=html_template_path
    )
    
@shared_task
def send_confirmation_email_task(company_name, applicant, to_email, role, joining_date, manager_name=None, resume_relative_path=None, html_template_relative__path=None):
    resume_path = os.path.join(settings.MEDIA_ROOT, resume_relative_path) if resume_relative_path else None
    html_template_path = os.path.join(settings.MEDIA_ROOT, html_template_relative__path) if html_template_relative__path else None
    send_confirmation_email(company_name, applicant, to_email, role, joining_date, manager_name, resume_path=resume_path, html_template_path=html_template_path)


@shared_task
def send_otp_mail_task(employee_name, to_email, otp, company_name):
    send_otp_mail(employee_name, to_email, otp, company_name)

@shared_task
def password_credentials_mailer_task(employee_name, to_email, username, password,manager):
    password_credentials_mailer(employee_name, to_email, username, password,manager)

@shared_task
def send_welcome_email_task(company_name, new_employee, to_email, role, manager_name, welcome_message, html_template_path=None):
    send_welcome_email(company_name, new_employee, to_email, role, manager_name, welcome_message, html_template_path)





