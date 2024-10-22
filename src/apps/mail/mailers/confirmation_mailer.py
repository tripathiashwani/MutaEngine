from email import encoders
from email.mime.base import MIMEBase
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from src import settings

from django.http import JsonResponse
<<<<<<<< HEAD:src/apps/applicant/confirmation_mailer.py
# from ..career import private
# company_email = private.company_email
# company_password = private.company_password   
========
from ..career import private
company_email = private.company_email
company_password = private.company_password   
>>>>>>>> 91c80a0938c66dff24b30473094044078ee2c680:src/apps/mailers/confirmation_mailer.py

# smtp_server = 'smtp.gmail.com'
# smtp_port = 587

company_email = settings.EMAIL_HOST_USER
company_password = settings.EMAIL_HOST_PASSWORD

smtp_server = settings.EMAIL_HOST
smtp_port = settings.EMAIL_PORT


def send_confirmation_email(company_name, applicant, to_email, role, manager_name, signed_offer_path=None, html_template_path=None):
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
                    '{{applicant}}': applicant,
                    '{{role}}': role,
                    '{{company_name}}': company_name,
                }

                
                for placeholder, replacement in replacements.items():
                    body = body.replace(placeholder, replacement)

        except Exception as e:
            print(f"Error reading the HTML template: {e}")
            body = default_body  # Fallback to default if any issue occurs
    else:
        body = default_body  # Use default if no HTML file is provided

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

