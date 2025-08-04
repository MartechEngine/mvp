from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Index, Integer, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import secrets
import hashlib
import enum

from app.models.base import Base, BaseMixin


class SessionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


class UserSession(Base, BaseMixin):
    __tablename__ = 'user_sessions'
    
    # Core identification
    user_id = Column(BaseMixin.id.type, ForeignKey('users.id'), nullable=False, index=True)
    
    # Session identification
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token_hash = Column(String(255), nullable=False, index=True)
    
    # Device and client information
    device_id = Column(String(255), nullable=True, index=True)
    device_name = Column(String(255), nullable=True)  # "iPhone 12", "Chrome on Windows"
    device_type = Column(String(50), nullable=True)   # "mobile", "desktop", "tablet"
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)    # IPv6 compatible
    
    # Session lifecycle
    expires_at = Column(DateTime, nullable=False, index=True)
    last_activity_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(Enum(SessionStatus), default=SessionStatus.ACTIVE, nullable=False, index=True)
    
    # Revocation tracking
    revoked_at = Column(DateTime, nullable=True)
    revoked_reason = Column(String(255), nullable=True)
    
    # Security and usage tracking
    refresh_count = Column(Integer, default=0, nullable=False)
    max_refresh_count = Column(Integer, default=1000, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='sessions')
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_sessions_user_status', 'user_id', 'status'),
        Index('idx_user_sessions_expires_at', 'expires_at'),
        Index('idx_user_sessions_session_id_status', 'session_id', 'status'),
    )
    
    @classmethod
    def generate_session_id(cls) -> str:
        """Generate a secure session ID."""
        return secrets.token_urlsafe(32)
    
    @classmethod
    def hash_refresh_token(cls, refresh_token: str) -> str:
        """Hash the refresh token for secure storage."""
        return hashlib.sha256(refresh_token.encode()).hexdigest()
    
    @classmethod
    def create_session(cls, user_id: str, device_info: dict = None) -> tuple['UserSession', str]:
        """Create a new user session with refresh token."""
        refresh_token = secrets.token_urlsafe(64)
        session = cls(
            user_id=user_id,
            session_id=cls.generate_session_id(),
            refresh_token_hash=cls.hash_refresh_token(refresh_token),
            expires_at=datetime.utcnow() + timedelta(days=30),  # 30 days
            device_id=device_info.get('device_id') if device_info else None,
            device_name=device_info.get('device_name') if device_info else None,
            device_type=device_info.get('device_type') if device_info else None,
            user_agent=device_info.get('user_agent') if device_info else None,
            ip_address=device_info.get('ip_address') if device_info else None,
        )
        return session, refresh_token
    
    def is_valid(self) -> bool:
        """Check if the session is valid (active and not expired)."""
        return (
            self.status == SessionStatus.ACTIVE and
            self.expires_at > datetime.utcnow() and
            self.refresh_count < self.max_refresh_count
        )
    
    def refresh(self, extend_days: int = 30) -> str:
        """Refresh the session and return a new refresh token."""
        if not self.is_valid():
            raise ValueError("Cannot refresh invalid session")
        
        new_refresh_token = secrets.token_urlsafe(64)
        self.refresh_token_hash = self.hash_refresh_token(new_refresh_token)
        self.expires_at = datetime.utcnow() + timedelta(days=extend_days)
        self.last_activity_at = datetime.utcnow()
        self.refresh_count += 1
        
        return new_refresh_token
    
    def revoke(self, reason: str = "user_logout"):
        """Revoke the session."""
        self.status = SessionStatus.REVOKED
        self.revoked_at = datetime.utcnow()
        self.revoked_reason = reason
    
    def expire(self):
        """Mark the session as expired."""
        self.status = SessionStatus.EXPIRED
        self.expires_at = datetime.utcnow()
    
    def update_activity(self, ip_address: str = None, user_agent: str = None):
        """Update last activity and optionally IP/user agent."""
        self.last_activity_at = datetime.utcnow()
        if ip_address:
            self.ip_address = ip_address
        if user_agent:
            self.user_agent = user_agent
