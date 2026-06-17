# ============================================================
# FILE: auth.py
# TOOLS USED:
#   - passlib     : Password hashing library (bcrypt algorithm)
#                   Never stores plain text passwords in the database
# ============================================================

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Convert plain text password to hashed version before storing."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if entered password matches the stored hashed password."""
    return pwd_context.verify(plain_password, hashed_password)