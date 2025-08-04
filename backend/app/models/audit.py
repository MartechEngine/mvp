from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseMixin


class AuditLog(Base, BaseMixin):
    """Audit log for tracking user actions and system events."""
    __tablename__ = 'audit_logs'

    user_id = Column(BaseMixin.id.type, ForeignKey('users.id'), nullable=True)
    organization_id = Column(BaseMixin.id.type, ForeignKey('organizations.id'), nullable=True)
    
    action = Column(String(100), nullable=False)  # e.g., 'user.login', 'user.update', 'organization.create'
    resource_type = Column(String(50), nullable=False)  # e.g., 'user', 'organization', 'project'
    resource_id = Column(String(100), nullable=True)  # ID of the affected resource
    
    # Additional context as JSON
    context_data = Column(JSON, default={})
    ip_address = Column(String(45))  # IPv6 support
    user_agent = Column(String(500))

    # Relationships
    user = relationship('User', backref='audit_logs')
    organization = relationship('Organization', backref='audit_logs')
