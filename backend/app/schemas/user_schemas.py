from pydantic import BaseModel, EmailStr, Field, ConfigDict
import uuid

# Base schema for a user, containing common fields
class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    full_name: str = Field(..., min_length=1, max_length=100, example="John Doe")

# Schema for creating a new user. Inherits from UserBase and adds the password.
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="a_strong_password")

# Schema for reading user data. This is what will be returned from the API.
# It excludes sensitive information like the password.
class UserRead(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    is_active: bool = Field(..., example=True)

    model_config = ConfigDict(from_attributes=True)

from typing import Optional, List
from uuid import UUID

from app.models.membership import MemberRole  # Import the enum from the model

# --- Base Schemas ---

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class OrganizationBase(BaseModel):
    name: str

# --- Request Schemas ---

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    organization_name: str = Field(..., min_length=2, description="The name of the user's initial organization.")

# --- Response Schemas ---

class User(UserBase):
    """Schema for a standard user profile response."""
    id: UUID
    is_active: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class Organization(OrganizationBase):
    """Represents an organization in API responses."""
    id: UUID
    owner_id: UUID

    model_config = ConfigDict(from_attributes=True)


class Membership(BaseModel):
    """Represents a user's membership within an organization."""
    role: MemberRole
    organization: Organization
    
    model_config = ConfigDict(from_attributes=True)

class UserWithMemberships(User):
    """A comprehensive user model including their organizational memberships."""
    memberships: List[Membership] = []
