from sqlalchemy import Column, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base, BaseMixin


class MemberRole(str, enum.Enum):
    """Organization roles for multi-tenancy."""
    OWNER = 'owner'
    ADMIN = 'admin'
    MEMBER = 'member'


class Membership(Base, BaseMixin):
    """Junction table linking users to organizations with roles."""
    __tablename__ = 'memberships'

    user_id = Column(BaseMixin.id.type, ForeignKey('users.id'), primary_key=True)
    organization_id = Column(BaseMixin.id.type, ForeignKey('organizations.id'), primary_key=True)
    
    role = Column(Enum(MemberRole), nullable=False, default=MemberRole.MEMBER)

    # Relationships
    user = relationship('User', back_populates='memberships')
    organization = relationship('Organization', back_populates='members')
