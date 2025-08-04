from pydantic import BaseModel, EmailStr, Field
import uuid

# Schema for the login request body
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="a_strong_password")

# Schema for the JWT token response
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Schema for the data contained within the JWT payload
class TokenPayload(BaseModel):
    sub: uuid.UUID

from .user_schemas import User  # Import the detailed User schema

# --- Request Schemas ---

class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str

class LogoutRequest(BaseModel):
    """Schema for logout request."""
    refresh_token: str

# --- Response Schemas ---


class Token(BaseModel):
    """Schema for JWT token pair response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginResponse(BaseModel):
    """The complete response for a successful login."""
    token: Token
    user: User


