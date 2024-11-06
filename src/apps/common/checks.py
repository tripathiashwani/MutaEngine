import magic  # This is from the python-magic library

def is_safe_pdf(file) -> bool:
    """
    Check if the given file is a safe PDF by:
    1. Checking the file extension
    2. Checking the MIME type
    3. Verifying the file's magic bytes (PDF header)
    """
    # Check if the file has a .pdf extension
    if not file.name.lower().endswith('.pdf'):
        return False

    # Check MIME type using python-magic
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(file.read(2048))  # Reads a small portion for MIME type detection
    file.seek(0)  # Reset file pointer to the beginning
    if mime_type != 'application/pdf':
        return False

    # Check file's magic bytes (first 4 bytes for PDF: %PDF)
    header = file.read(4)
    file.seek(0)  # Reset file pointer again after reading
    if header != b'%PDF':
        return False

    return True
