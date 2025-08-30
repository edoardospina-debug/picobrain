from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings - these will be imported from config when needed
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None,
    secret_key: str = None
) -> str:
    """Create JWT access token"""
    # Import here to avoid circular dependency
    if secret_key is None:
        from app.core.config import settings
        secret_key = settings.SECRET_KEY
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
    secret_key: str = None
) -> str:
    """Create JWT refresh token"""
    # Import here to avoid circular dependency
    if secret_key is None:
        from app.core.config import settings
        secret_key = settings.SECRET_KEY
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh"
    }
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, token_type: str = "access", secret_key: str = None) -> Optional[str]:
    """Verify JWT token and return subject"""
    # Import here to avoid circular dependency
    if secret_key is None:
        from app.core.config import settings
        secret_key = settings.SECRET_KEY
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        subject: str = payload.get("sub")
        token_type_claim: str = payload.get("type")
        
        if subject is None or token_type_claim != token_type:
            return None
        return subject
    except JWTError:
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against hashed"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)
