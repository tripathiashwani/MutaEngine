import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
from src import settings
import os

from django.http import JsonResponse

company_email = settings.EMAIL_HOST_USER
company_password = settings.EMAIL_HOST_PASSWORD

smtp_server = settings.EMAIL_HOST
smtp_port = settings.EMAIL_PORT


def send_offer_letter(company_name, applicant, applicant_id, to_email,role, department,start_date , supervisor,location,job_template_id,base_salary,performance_bonus, resume_path=None, offer_letter_path=None, html_template_path=None):
    print(html_template_path,"html_template_path in mailer")
    subject = f"Offer Letter for {role} at {company_name}"
    
    # Default body if no HTML file is provided
    default_body = f"""
    Dear {applicant},<br><br>
    
    We are pleased to extend an offer for the <strong>{role}</strong> position at <strong>{company_name}</strong>! Below are the details of your offer:<br><br>
    {f'<strong>Base Salary:</strong><br>{base_salary}<br><br>' if base_salary else ''}
    {f'<strong>Performance Bonus:</strong><br>{performance_bonus}<br><br>' if performance_bonus else ''}
    

    
    <strong><a href="{f"https://career.mutaengine.cloud/career/{job_template_id}/offer-letter-signed-form"}" target="_blank">Submit Signed offer letter</a><strong>
    
    We are excited to have you on board and look forward to your acceptance.<br><br>
    
    If you have any questions, feel free to reach out to us.<br><br>
    
    Best regards,<br>
    <strong>{supervisor}</strong><br>
    Hiring Manager at {company_name}<br>
    {company_email}<br>
    """

    # Check if an HTML template path is provided
    if html_template_path and os.path.exists(html_template_path):
        try:
            # Read the HTML file content
            with open(html_template_path, 'r', encoding='utf-8') as html_file:
                body = html_file.read()

                # Replace placeholders in the HTML template
                replacements = {
                    '{{ applicant }}': applicant,
                    '{{ role }}': role or 'N/A',
                    '{{ company_name }}': company_name or 'N/A',
                    '{{ manager_name }}': supervisor or 'N/A',
                    '{{ start_date }}': 'N/A', 
                    '{{ salary }}': base_salary or 'N/A',
                    '{{ location }}': 'Remote'  
                }

                
                for placeholder, replacement in replacements.items():
                    body = body.replace(placeholder, replacement)

        except Exception as e:
            print(f"Error reading the HTML template: {e}")
            body = default_body  
    else:
        body = default_body  

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = formataddr((company_name, company_email))
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body as HTML
    msg.attach(MIMEText(body, 'html'))

    # Handle offer letter attachment if provided
    if offer_letter_path and os.path.exists(offer_letter_path):
        try:
            with open(offer_letter_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(offer_letter_path)}')
                msg.attach(part)
        except Exception as e:
            print(f"Error reading the attachment: {e}")
    if resume_path and os.path.exists(resume_path):
        try:
            with open(resume_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(resume_path)}')
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
        print(f"offerletter email sent to {applicant} at {to_email}")
        return JsonResponse({'message': 'success'}, status=200)
    except Exception as e:
        print(f"Failed to send email: {e}")
        return JsonResponse({'message': 'Failed'}, status=500)

