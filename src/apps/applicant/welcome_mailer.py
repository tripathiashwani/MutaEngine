import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import os

company_email = ''  
company_password = ''      

smtp_server = 'smtp.gmail.com'
smtp_port = 587


def send_welcome_email(company_name, new_employee, to_email, role, manager_name, welcome_message, html_template_path=None):
    subject = f"Welcome to {company_name}, {new_employee}!"

    # Default body if no HTML file is provided
    default_body = f"""
    Dear {new_employee},<br><br>
    I wanted to take a take a moment to personally welcome you to the <strong>{company_name}</strong> team! We are thrilled to have you join us as a <strong>{role}</strong>.<br><br>
    We have some exciting projects lined up, and your skills and expertise will be a valuable addition to our team. Your role as a <strong>{role}</strong> will play a key part in our continued success.<br><br>
    In the next few days ,we will schedule an orientation session to help you get acquainted with our team, culture, and processes. If you have any questions or need assistance, please don't hesitate to reach out.<br><br>
    
    onece again, welcome aboard!<br><br>
    
    Best regards,<br>
    <strong>{manager_name}</strong><br>
    Hiring Manager at {company_name}<br>
    {company_email}<br>
    """

    # Check if an HTML template path is provided
    if html_template_path and os.path.exists(html_template_path):
        try:
            # Read the HTML file content
            with open(html_template_path, 'r', encoding='utf-8') as html_file:
                body = html_file.read()
        except Exception as e:
            print(f"Error reading the HTML template: {e}")
            body = default_body  # Fallback to default if any issue occurs
    else:
        body = default_body  # Use default if no HTML file is provided

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = formataddr((company_name, company_email))
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body as HTML
    msg.attach(MIMEText(body, 'html'))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(company_email, company_password)
        text = msg.as_string()
        server.sendmail(company_email, to_email, text)
        server.quit()
        print(f"Welcome email sent to {new_employee} at {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


