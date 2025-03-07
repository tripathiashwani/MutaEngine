from email import encoders
from email.mime.base import MIMEBase
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from src import settings

from django.http import JsonResponse

company_email = settings.EMAIL_HOST_USER
company_password = settings.EMAIL_HOST_PASSWORD

smtp_server = settings.EMAIL_HOST
smtp_port = settings.EMAIL_PORT


def send_confirmation_email(company_name, applicant, to_email, role, joining_date, manager_name=None, resume_path=None, html_template_path=None,signed_offer_path=None):
    subject = f"Offer Acceptance Confirmation for {role} at {company_name}"

    # If an HTML template is provided, use that; otherwise use the default body
    default_body = f"""
        Dear {applicant},<br><br>

        Congratulations on accepting the offer for the <strong>{role}</strong> position at <strong>{company_name}</strong>! We have successfully received your signed offer acceptance letter.<br><br>
        
        We are excited to welcome you to the team and look forward to working with you. Our HR team will be in touch with the next steps, including the onboarding process.<br><br>

        If you have any questions or require further assistance, please don't hesitate to reach out to us.<br><br>

        Once again, welcome aboard!<br><br>

        Best regards,<br>
        <strong>{manager_name}</strong><br>
        Hiring manager at {company_name}<br>
        """


    if html_template_path and os.path.exists(html_template_path):
        try:
            # Read the HTML file content
            with open(html_template_path, 'r', encoding='utf-8') as html_file:
                body = html_file.read()

                # Replace placeholders in the HTML template
                replacements = {
                    '{{ applicant }}': applicant or 'Applicant',
                    '{{ role }}': role or 'backend developer',
                    '{{ company_name }}': company_name or 'Mutaengine',
                    '{{ manager_name }}': manager_name or 'Manager',
                    '{{ start_date }}':joining_date or '2022-01-01',
                }

                
                for placeholder, replacement in replacements.items():
                    body = body.replace(placeholder, replacement)

        except Exception as e:
            print(f"Error reading the HTML template: {e}")
            body = default_body  
    else:
        body = default_body 

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = formataddr((company_name, company_email))
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Attach the signed offer letter if provided
    if signed_offer_path:
        try:
            with open(signed_offer_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={signed_offer_path}')
                msg.attach(part)
        except Exception as e:
            print(f"Error reading the attachment: {e}")

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(company_email, company_password)
        text = msg.as_string()
        server.sendmail(company_email, to_email, text)
        server.quit()
        print(f"Confirmation email sent to {applicant} at {to_email}")
        return JsonResponse({'message': 'success'}, status=200)
    except Exception as e:
        print(f"Failed to send email: {e}")
        return JsonResponse({'message': 'Failed'}, status=500)

