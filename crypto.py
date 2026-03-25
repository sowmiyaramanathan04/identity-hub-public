import hashlib
from cryptography.fernet import Fernet


CLAIM_AES_KEY = b'6Z0uF5s5E8mHnR5KcZzM9xZJmJH0Kk4KZkP8b7Qy0lY='
cipher = Fernet(CLAIM_AES_KEY)

def generate_duid(citizen_id: str, system_salt: str) -> str:
    raw = citizen_id + system_salt
    return hashlib.sha256(raw.encode()).hexdigest()

def encrypt_value(value: str) -> str:
    return cipher.encrypt(value.encode()).decode()

def decrypt_value(value: str) -> str:
    return cipher.decrypt(value.encode()).decode()

def hash_metadata(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()
