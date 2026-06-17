# FILE: auth.py
# TOOLS USED: bcrypt for password hashing

import hashlib
import hmac
import os

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    password = password[:72]  # bcrypt limit fix
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ':' + key.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    try:
        plain_password = plain_password[:72]
        salt_hex, key_hex = hashed_password.split(':')
        salt = bytes.fromhex(salt_hex)
        key = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        return key.hex() == key_hex
    except:
        return False