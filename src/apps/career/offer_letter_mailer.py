import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import os


from django.http import JsonResponse

company_email = 'mail' 
company_password = 'password_for smtp'


smtp_server = 'smtp.gmail.com'
smtp_port = 587


def send_offer_letter(company_name, applicant, to_email, role, offer_details, manager_name, offer_letter_path=None, html_template_path=None):
    subject = f"Offer Letter for {role} at {company_name}"
    
    # Default body if no HTML file is provided
    default_body = f"""
    Dear {applicant},<br><br>
    
    We are pleased to extend an offer for the <strong>{role}</strong> position at <strong>{company_name}</strong>! Below are the details of your offer:<br><br>
    
    <strong>Offer Details:</strong><br>
    {offer_details}<br><br>
    
    We are excited to have you on board and look forward to your acceptance.<br><br>
    
    If you have any questions, feel free to reach out to us.<br><br>
    
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

                # Replace placeholders in the HTML template
                replacements = {
                    '{{ applicant }}': applicant,
                    '{{ role }}': role,
                    '{{ company_name }}': company_name,
                    '{{ manager_name }}': manager_name,
                    '{{ start_date }}': 'N/A', 
                    '{{ salary }}': offer_details.split(':')[1].strip(),  
                    '{{ location }}': 'Remote'  
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


# Example usage
if __name__ == "__main__":
    company_name = "Mutaengine"
    applicant = "John Doe"
    to_email = "csaifw21004@glbitm.ac.in"
    role = "Software Engineer"
    offer_details = "Annual Salary: $100,000"
    manager_name = "Jane Smith"
    current_directory = os.path.dirname(__file__)
    offer_letter_path = os.path.join(current_directory, "test_file.pdf")
    html_template_path = os.path.join(current_directory, "template.html")


    send_offer_letter(company_name, applicant, to_email, role, offer_details, manager_name, offer_letter_path, html_template_path)
