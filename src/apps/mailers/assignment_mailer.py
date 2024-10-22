import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import os

from django.http import JsonResponse
from ..career import private
company_email = private.company_email
company_password = private.company_password

smtp_server = 'smtp.gmail.com'
smtp_port = 587


def send_assignment(company_name, applicant, to_email, role, last_date, assignment_detail_link, application_id, resume_path=None, html_template_path=None):
    subject = f"Assignment for {role} at {company_name}"
    
    # Default body if no HTML file is provided
    default_body = f"""
        Dear {applicant},<br><br>
        
        We hope this email finds you well. 
        Attached below are the details of the assignment for the <strong>{role}</strong> position at <strong>{company_name}</strong>.<br><br>
        kindly submit your assignment before the deadline.<br><br>
        Your application ID is: {application_id}<br><br>
        <strong>Assignment Objective:</strong><br>
        we want to evaluate your problem solving skills, your ability to build secure and scalable systems. This assignment is designed to assess how you approach towards real world problems,
        code quality and best practices.<br><br>
        <strong>Assignment Details:</strong><br>
        {assignment_detail_link}<br><br>
        
        <strong>Submission Deadline:</strong> {last_date}<br>
       
        We look forward to receiving your submission. Should you have any questions, please don't hesitate to reach out.<br><br>
        
        Best regards,<br>
        <strong>{company_name}</strong><br>
        {company_email}
        """

    # Check if an HTML template path is provided
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
                    '{{assignment}}': assignment,
                    '{{last_date}}': last_date,
                    '{{submission_link}}': f'<a href="{submission_link}">Submit your assignment here</a>',
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
    msg['From'] = formataddr((company_name, company_email))
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    
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
        print(f"assignment sent to {applicant} at {to_email}")
        return JsonResponse({'message': 'success'}, status=200)
    except Exception as e:
        print(f"Failed to send email: {e}")
        return JsonResponse({'message': 'Failed'}, status=500)


# Example usage
if __name__ == "__main__":
    company_name = "TechCorp"
    applicant = "John Doe"
    to_email = "applicant@example.com"
    role = "Software Engineer"
    assignment = "Please complete the coding challenge attached."
    last_date = "October 20, 2024"
    submission_link = "http://submissionlink.com"
    
    current_directory = os.path.dirname(__file__)
    resume_path = os.path.join(current_directory, "test_file.pdf")  # Path to your PDF file
    html_template_path = os.path.join(current_directory, "assignment_template.html")  # Path to your HTML template

    send_assignment(company_name, applicant, to_email, role, assignment, last_date, submission_link, resume_path, html_template_path)