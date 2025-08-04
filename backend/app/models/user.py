from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseMixin


class User(Base, BaseMixin):
    __tablename__ = 'users'

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # A user can be a member of multiple organizations
    memberships = relationship('Membership', back_populates='user', cascade='all, delete-orphan')
    
    # User can have multiple active sessions
    sessions = relationship('UserSession', back_populates='user', cascade='all, delete-orphan')
