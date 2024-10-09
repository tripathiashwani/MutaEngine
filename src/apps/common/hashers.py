import base64

from cryptography.fernet import Fernet
from django.conf import settings


def encrypt_password(raw_password: str):
    key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].encode())
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(raw_password.encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password: str):
    key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].encode())
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password.encode())
    return decrypted_password.decode()
