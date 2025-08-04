from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# --- Password Hashing ---

# Initialize a CryptContext for password hashing using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashes a plain-text password."""
    return pwd_context.hash(password)


# --- JSON Web Tokens (JWT) ---

ALGORITHM = "HS256"


def create_access_token(
    subject: str, expires_delta: Optional[timedelta] = None, additional_claims: Optional[dict] = None
) -> str:
    """
    Creates a new access token.

    Args:
        subject (str): The subject of the token (e.g., user ID).
        expires_delta (Optional[timedelta]): The lifespan of the token. Defaults to settings.
        additional_claims (Optional[dict]): Additional claims to include in the token payload.

    Returns:
        str: The encoded JWT access token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    if additional_claims:
        to_encode.update(additional_claims)

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY.get_secret_value(), algorithm=ALGORITHM
    )
    return encoded_jwt


# NOTE: Refresh tokens are NOT handled as JWTs in this system.
# Instead, they are managed as secure random tokens by the UserSessionService.
# This provides better security through token rotation and session revocation capabilities.
# See: 2.5.1-Backend-User-Session-Service.md for refresh token implementation.


def decode_token(token: str) -> Optional[dict]:
    """
    Decodes a JWT token.

    Args:
        token (str): The JWT to decode.

    Returns:
        Optional[dict]: The decoded token payload if valid, otherwise None.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        # This will catch expired tokens, invalid signatures, etc.
        return None

# This provides better security through token rotation and session revocation capabilities.
# See: 2.5.1-Backend-User-Session-Service.md for refresh token implementation.

def decode_token(token: str) -> Optional[dict]:
    """
    Decodes a JWT token.
    
    Args:
        token (str): The JWT to decode.
        
    Returns:
        Optional[dict]: The decoded token payload if valid, otherwise None.
    """
    try:
        # Handle both SecretStr and regular str types for SECRET_KEY
        secret_key = settings.SECRET_KEY
        if hasattr(secret_key, 'get_secret_value'):
            secret_key = secret_key.get_secret_value()
        
        payload = jwt.decode(token, str(secret_key), algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # This will catch expired tokens, invalid signatures, etc.
        return None
