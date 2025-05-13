from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.FERNET_KEY)

def encrypt_location(plain_text):
    return fernet.encrypt(plain_text.encode()).decode()

def decrypt_location(cipher_text):
    return fernet.decrypt(cipher_text.encode()).decode()