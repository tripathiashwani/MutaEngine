import os
import re
import uuid

from decouple import config
from django.core.exceptions import ValidationError

import markdown
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa


def image_validate(image):
    check_exts = (".jpg", ".jpeg", ".png")
    file_extension = os.path.splitext(str(image))

    MAX_IMAGE_SIZE = config("MAX_IMAGE_SIZE", cast=int, default=1000000)

    if image.size >= MAX_IMAGE_SIZE:
        raise ValidationError(f"File should be less then {MAX_IMAGE_SIZE//1000000}MB")
    if (
        file_extension[1] == check_exts[0]
        or file_extension[1] == check_exts[1]
        or file_extension[1] == check_exts[2]
    ):
        pass
    else:
        raise ValidationError("Provide Valid Image file such as jpeg, jpg, png")
    if image:
        pass
    else:
        raise ValidationError("Image is not provided")


def modify_string(input_string) -> str:
    # Replace spaces with hyphens
    replaced_string = input_string.replace(" ", "-")

    # Remove special characters using regular expression
    cleaned_string = re.sub(r"[^\w\s-]", "", replaced_string)
    return cleaned_string


def get_upload_folder(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{str(uuid.uuid4())}.{ext}"

    model_path = ""
    if hasattr(instance, "_meta"):  # Check if instance has a Meta class
        app_label = instance._meta.app_label
        model_name = instance._meta.model_name
        model_path = os.path.join(app_label, model_name)

    return "/".join([model_path, filename])


def generate_pdf(content, placeholders):
    # Step 1: Replace placeholders with actual data
    for key, value in placeholders.items():
        content = content.replace(f"[{key}]", str(value))

    # Step 2: Convert HTML to PDF
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(content, dest=pdf_buffer)
    
    # Check for any errors
    if pisa_status.err:
        return None

    # Move the buffer pointer to the beginning
    pdf_buffer.seek(0)
    return pdf_buffer