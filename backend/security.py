import jwt
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from typing import Optional
from config import Config
import os

# Session encryption key
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
cipher = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)

def encrypt_session_data(data: str) -> str:
    """Encrypts session data before storage"""
    return cipher.encrypt(data.encode()).decode()

def decrypt_session_data(encrypted_data: str) -> str:
    """Decrypts session data"""
    return cipher.decrypt(encrypted_data.encode()).decode()

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Creates JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verifies JWT token and returns user_id"""
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except jwt.InvalidTokenError:
        return None

class DataHandling:
    """Minimal data collection principles"""
    
    # Only collect essential fields
    ESSENTIAL_FIELDS = {
        "email", "age", "grade_level", 
        "parent_email", "parent_consent_given"
    }
    
    # Never log
    DO_NOT_LOG = {
        "passwords", "tokens", "conversation_history"
    }
    
    @staticmethod
    def sanitize_input(data: dict) -> dict:
        """Only keep essential fields"""
        return {k: v for k, v in data.items() if k in DataHandling.ESSENTIAL_FIELDS}
    
    @staticmethod
    def should_persist(field: str) -> bool:
        """Check if field should be stored"""
        return field not in DataHandling.DO_NOT_LOG
