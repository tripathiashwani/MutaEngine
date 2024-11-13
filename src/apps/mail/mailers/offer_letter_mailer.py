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


def send_offer_letter(company_name, company_logo, comapny_linkedin_url, applicant, applicant_id, to_email,role, department,start_date , supervisor,location,job_template_id,base_salary,performance_bonus, resume_path=None, offer_letter_path=None, html_template_path=None):
    print(html_template_path,"html_template_path in mailer")
    subject = f"Offer Letter for {role} at {company_name}"
    
    # Default body if no HTML file is provided
    default_body = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assignment Email</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f5;">

    <table align="center" style="width: 100%; background-color: #f4f4f5; padding: 20px;">
        <tr>
        <td align="center">
            <table style="max-width: 600px; width: 100%; background-color: #ffffff; border-radius: 8px; overflow: hidden;">
            <tr>
                <td style="padding: 40px 20px; text-align: center; background-color: #ffffff;">
                <img src="{ company_logo }" alt="{company_name} Logo" style="display: block; margin: 0 auto;">
                <a href="{ comapny_linkedin_url }"></a><img src="https://via.placeholder.com/20" alt="LinkedIn Icon" style="display: inline-block; float: right;">
                </td>
            </tr>

            <tr>
        <td style="padding: 20px; text-align: left; color: #333;">
        <p style="font-size: 18px;"><strong>Subject:</strong> Congratulations! Offer of employment at {company_name}e.</p>
        <p>Dear <strong>{applicant}</strong>,</p>
        <p>I hope this email finds you well.</p>
        <p>
            We are pleased to inform you that after careful consideration, we are delighted to offer you the position of <strong>{role}</strong> at MutaEngine. We were truly impressed with your skills, experience, and problem-solving abilities, and we are excited to have you join our innovative team.
        </p>
        <p>
            Attached to this email, you will find your offer letter, which outlines the terms and conditions of your employment, including your CTC and other relevant details. Kindly review the document thoroughly.
        </p>
        <p>
            To formally accept this offer, please sign the offer letter and upload it through the following link.
        </p>

        <h3 style="color: #333; font-size: 16px; margin-top: 20px;">Submit Signed Offer Letter here :</h3>
        <p><a href="https://career.mutaengine.cloud/career/{job_template_id}/offer-letter-signed-form" style="color: #007bff; text-decoration: none;">https://career.mutaengine.cloud/career/{job_template_id}/offer-letter-signed-form</a></p>
        <p style="text-align: center; margin: 20px 0;">
            <a href="https://career.mutaengine.cloud/career/{job_template_id}/offer-letter-signed-form" style="text-decoration: none;">
            <button style="padding: 12px 24px; font-size: 16px; color: #ffffff; background-color: #6200ea; border: none; border-radius: 5px; cursor: pointer;">
                Submit Signed Offer Letter
            </button>
            </a>
        </p>

        <p>We look forward to receiving your confirmation and welcoming you to the {company_name} family!</p>
        <p>If you have any questions or need clarification, feel free to reach out.</p>
        </td>
    </tr>

    <tr>
        <td style="padding: 20px; text-align: left; color: #333; border-top: 1px solid #ddd;">
        <p>Best Regards,<br>{supervisor}<br>Hiring Manager <strong>@{company_name}</strong></p>
        </td>
    </tr>
    <tr>
            <td style="padding: 20px; text-align: center; background-color: #f4f4f5;">
              <a href="#"><img src="https://via.placeholder.com/20" alt="LinkedIn Icon" style="vertical-align: middle;"></a>
              <p style="color: #777; font-size: 12px; margin-top: 10px;">
                © 2024 { company_name }. All rights reserved.
              </p>
              <p style="color: #777; font-size: 12px;">
                <a href="{ comapny_linkedin_url }" style="color: #007bff; text-decoration: none;">Follow us on LinkedIn</a> | 
                <a href="#" style="color: #007bff; text-decoration: none;">Privacy Policy</a> |
                <a href="#" style="color: #007bff; text-decoration: none;">Terms of Service</a> |
                <a href="#" style="color: #007bff; text-decoration: none;">Contact Us</a> |
                <a href="#" style="color: #007bff; text-decoration: none;">Website URL</a>
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>

</body>
</html>
    '''

    # Check if an HTML template path is provided
    if html_template_path and os.path.exists(html_template_path):
        try:
            # Read the HTML file content
            with open(html_template_path, 'r', encoding='utf-8') as html_file:
                body = html_file.read()

                # Replace placeholders in the HTML template
                replacements = {
                    # '{{ applicant }}': applicant,
                    # '{{ role }}': role or 'N/A',
                    # '{{ company_name }}': company_name or 'N/A',
                    # '{{ manager_name }}': supervisor or 'N/A',
                    # '{{ start_date }}': 'N/A', 
                    # '{{ salary }}': base_salary or 'N/A',
                    # '{{ location }}': 'Remote'  
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

