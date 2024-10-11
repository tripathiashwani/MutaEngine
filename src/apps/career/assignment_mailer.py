import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import time

# Your Gmail credentials
company_email = ''  
company_password = ''      

# Gmail SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Function to send email
def send_email(company_name, applicant, to_email, role, assignment, last_date, submission_link, resume_path):
    subject = f"Assignment for {role} at {company_name}"
    
    body = f"""
    Dear {applicant},<br><br>
    
    We hope this email finds you well. Below is the assignment for the <strong>{role}</strong> position at <strong>{company_name}</strong>.<br><br>
    
    <strong>Assignment Details:</strong><br>
    {assignment}<br><br>
    
    <strong>Submission Deadline:</strong> {last_date}<br>
    <strong>Submission Link:</strong> <a href="{submission_link}">Submit your assignment here</a><br><br>
    
    We look forward to receiving your submission. Should you have any questions, please don't hesitate to reach out.<br><br>
    
    Best regards,<br>
    <strong>{company_name}</strong>
    {company_email}<br>
    """

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = formataddr((company_name, company_email))
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body with HTML content
    msg.attach(MIMEText(body, 'html'))

    # Attach the resume (if provided)
    if resume_path:
        try:
            attachment = open(resume_path, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {resume_path}')
            msg.attach(part)
        except Exception as e:
            print(f"Error reading the attachment: {e}")

    # Connect to the Gmail server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(company_email, company_password)
        text = msg.as_string()
        server.sendmail(company_email, to_email, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")



company_name = "XYZ Tech"
applicant = "John Doe"
to_email = "johndoe@example.com"
role = "Back-End Developer"
assignment = "Please complete the following back-end task using Django."
last_date = "2024-10-20"
submission_link = "https://submission-link.com"
resume_path = "resume.pdf"

# Sending email with assignment details
send_email(company_name, applicant, to_email, role, assignment, last_date, submission_link, resume_path)
