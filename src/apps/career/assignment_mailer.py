import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import time


company_email = ''  
company_password = ''      


smtp_server = 'smtp.gmail.com'
smtp_port = 587


def send_email(company_name, applicant, to_email, role, assignment, last_date, submission_link, resume_path,html_template_path=None):
    subject = f"Assignment for {role} at {company_name}"
    
    if html_template_path:
        try:
            with open(html_template_path, 'r', encoding='utf-8') as html_file:
                body = html_file.read()
                # Optionally replace placeholders in the HTML template
                body = (body.replace('{{applicant}}', applicant)
                            .replace('{{role}}', role)
                            .replace('{{company_name}}', company_name)
                )
        except Exception as e:
            print(f"Error reading the HTML template: {e}")
            return
    else:
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

    
    msg = MIMEMultipart()
    msg['From'] = formataddr((company_name, company_email))
    msg['To'] = to_email
    msg['Subject'] = subject

   
    msg.attach(MIMEText(body, 'html'))

    
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

    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(company_email, company_password)
        text = msg.as_string()
        server.sendmail(company_email, to_email, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")



