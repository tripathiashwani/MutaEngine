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

def send_assignment(company_name, applicant, to_email, role, last_date, assignment_detail_link,assignment_detail, application_id, start_date=None, salary=None, location=None, manager_name=None, resume_path=None, html_template_path=None):
    subject = f"Assignment for {role} at {company_name}"
    print("at send_assignment")
    print(resume_path,"resume_path at send_assignment")
    # Default body if no HTML file is provided
    default_body = f"""
        Dear {applicant},<br><br>
        We hope this email finds you well. 
        Attached below are the details of the assignment for the <strong>{role}</strong> position at <strong>{company_name}</strong>.<br><br>
        Kindly submit your assignment before the deadline.<br><br>

        <strong>Application ID:</strong> {application_id}<br>
        
        <strong>Assignment Details:</strong><br>
        {assignment_detail}<br><br>
        <strong>Assignment Link:</strong> <a href="{assignment_detail_link}">{assignment_detail_link}</a><br><br>
        <strong>Submission Deadline:</strong> {last_date}<br>
        Best regards,<br>
        <strong>{company_name}</strong><br>
        {company_email}
        """

    # Check if an HTML template path is provided
    if html_template_path and os.path.exists(html_template_path):
        print("HTML template path provided")
        try:
            # Read the HTML file content
            with open(html_template_path, 'r', encoding='utf-8') as html_file:
                body = html_file.read()

                # Replace placeholders in the HTML template
                replacements = {
                    '{{ applicant }}': applicant,
                    '{{ role }}': role,
                    '{{ company_name }}': company_name,
                    '{{ start_date }}': start_date or 'N/A',
                    '{{ salary }}': salary or 'N/A',
                    '{{ location }}': location or 'N/A',
                    '{{ manager_name }}': manager_name or 'N/A',
                    '{{ last_date }}': last_date,
                    '{{ assignment_detail_link }}': assignment_detail_link or 'N/A',
                    '{{ assignment_detail }}': assignment_detail or 'N/A'

                }

                for placeholder, replacement in replacements.items():
                    body = body.replace(placeholder, replacement)

        except Exception as e:
            print(f"Error reading the HTML template: {e}")
            body = default_body  # Fallback to default if any issue occurs
    else:
        body = default_body  # Use default if no HTML file is provided

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = formataddr((company_name, company_email)) # type: ignore
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    # Attach resume if provided
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
        server = smtplib.SMTP(smtp_server, smtp_port) # type: ignore
        server.starttls()
        server.login(company_email, company_password) # type: ignore
        text = msg.as_string()
        server.sendmail(company_email, to_email, text) # type: ignore
        server.quit()
        print(f"Assignment sent to {applicant} at {to_email}")
        return JsonResponse({'message': 'success'}, status=200)
    except Exception as e:
        print(f"Failed to send email: {e}")
        return JsonResponse({'message': 'Failed'}, status=500)
