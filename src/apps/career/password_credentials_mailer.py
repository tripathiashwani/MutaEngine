import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from . import private
company_email = private.company_email
company_password = private.company_password       

# Gmail SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Function to send email with login credentials
def password_credentials_mailer(employee_name, to_email, username, password,manager):
    subject = "Your Login Credentials"
    
    body = f"""
    Dear {employee_name},<br><br>

    Welcome to the team! We are pleased to provide you with your login credentials to access the company systems.<br><br>

    <strong>Username:</strong> {username}<br>
    <strong>Password:</strong> {password}<br><br>

    Please make sure to log in and change your password at your earliest convenience.<br><br>

    If you have any issues accessing your account or need further assistance, feel free to reach out to our IT support team.<br><br>

    Best regards,<br>
    <strong>{manager}</strong><br>
    
    {company_email}<br>
    """

    
    msg = MIMEMultipart()
    msg['From'] = formataddr((manager, company_email))
    msg['To'] = to_email
    msg['Subject'] = subject

    
    msg.attach(MIMEText(body, 'html'))

    # Connect to the Gmail server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(company_email, company_password)
        text = msg.as_string()
        server.sendmail(company_email, to_email, text)
        server.quit()
        print(f"Login credentials email sent to {employee_name} at {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")



