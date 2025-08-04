import logging
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.core.config import settings
from app.core.exceptions import InvalidCredentialsError, ValidationError
from app.models.user_session import UserSession, SessionStatus
from app.models.user import User

logger = logging.getLogger(__name__)


class UserSessionService:
    """Service for managing user sessions and refresh tokens."""
    
    def __init__(self, db: Session):
        self.db = db
        self.max_sessions_per_user = getattr(settings, 'MAX_SESSIONS_PER_USER', 5)
        self.refresh_token_expire_days = getattr(settings, 'REFRESH_TOKEN_EXPIRE_DAYS', 30)
    
    def create_session(self, user_id: str, device_info: dict, 
                      ip_address: Optional[str] = None) -> Tuple[UserSession, str]:
        """
        Create a new user session with refresh token.
        
        Args:
            user_id: The user's UUID
            device_info: Dictionary containing device metadata
            ip_address: Client IP address
            
        Returns:
            Tuple of (UserSession, refresh_token_string)
            
        Raises:
            ValidationError: If session limit exceeded
        """
        try:
            # Check session limits
            active_sessions_count = self.db.query(UserSession).filter(
                and_(
                    UserSession.user_id == user_id,
                    UserSession.status == SessionStatus.ACTIVE,
                    UserSession.expires_at > datetime.utcnow()
                )
            ).count()
            
            if active_sessions_count >= self.max_sessions_per_user:
                # Terminate oldest session to make room
                oldest_session = self.db.query(UserSession).filter(
                    and_(
                        UserSession.user_id == user_id,
                        UserSession.status == SessionStatus.ACTIVE
                    )
                ).order_by(UserSession.last_activity_at.asc()).first()
                
                if oldest_session:
                    self._terminate_session(oldest_session, "Session limit exceeded")
            
            # Use the UserSession model's create_session method
            session, refresh_token = UserSession.create_session(
                user_id=user_id,
                device_info={
                    "device_id": device_info.get("device_id"),
                    "device_name": device_info.get("device_name", "Unknown Device"),
                    "device_type": device_info.get("device_type", "unknown"),
                    "user_agent": device_info.get("user_agent"),
                    "ip_address": ip_address
                }
            )
            
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
            
            logger.info(f"Created session {session.session_id} for user {user_id}")
            
            return session, refresh_token
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create session for user {user_id}: {e}")
            raise
    
    def refresh_session(self, refresh_token: str, 
                       ip_address: Optional[str] = None) -> Tuple[UserSession, str]:
        """
        Refresh a session and rotate the refresh token.
        
        Args:
            refresh_token: The current refresh token
            ip_address: Client IP address
            
        Returns:
            Tuple of (UserSession, new_refresh_token)
            
        Raises:
            InvalidCredentialsError: If refresh token is invalid or expired
        """
        try:
            # Find session by refresh token hash
            token_hash = self._hash_token(refresh_token)
            session = self.db.query(UserSession).filter(
                and_(
                    UserSession.refresh_token_hash == token_hash,
                    UserSession.status == SessionStatus.ACTIVE,
                    UserSession.expires_at > datetime.utcnow()
                )
            ).first()
            
            if not session:
                logger.warning(f"Invalid refresh token attempt from IP {ip_address}")
                raise InvalidCredentialsError("Invalid or expired refresh token")
            
            # Check if session is valid using the model method
            if not session.is_valid():
                logger.warning(f"Session {session.session_id} is no longer valid")
                raise InvalidCredentialsError("Session is no longer valid")
            
            # Check for suspicious activity (IP change)
            if ip_address and session.ip_address and ip_address != session.ip_address:
                logger.warning(f"IP address changed for session {session.session_id}: {session.ip_address} -> {ip_address}")
                # Could implement additional security measures here
            
            # Use the UserSession model's refresh method
            new_refresh_token = session.refresh()
            
            # Update IP address if provided
            if ip_address:
                session.update_activity(ip_address=ip_address)
            
            self.db.commit()
            
            logger.info(f"Refreshed session {session.session_id}")
            
            return session, new_refresh_token
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to refresh session: {e}")
            raise
    
    def terminate_session(self, refresh_token: str) -> bool:
        """
        Terminate a session (logout).
        
        Args:
            refresh_token: The refresh token to terminate
            
        Returns:
            True if session was terminated, False if not found
        """
        try:
            token_hash = self._hash_token(refresh_token)
            session = self.db.query(UserSession).filter(
                UserSession.refresh_token_hash == token_hash
            ).first()
            
            if session:
                session.revoke("User logout")
                self.db.commit()
                logger.info(f"Terminated session {session.session_id}: User logout")
                return True
            
            return False
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to terminate session: {e}")
            return False
    
    def terminate_all_sessions(self, user_id: str, except_session_id: Optional[str] = None) -> int:
        """
        Terminate all active sessions for a user.
        
        Args:
            user_id: The user's UUID
            except_session_id: Optional session ID to keep active
            
        Returns:
            Number of sessions terminated
        """
        try:
            query = self.db.query(UserSession).filter(
                and_(
                    UserSession.user_id == user_id,
                    UserSession.status == SessionStatus.ACTIVE
                )
            )
            
            if except_session_id:
                query = query.filter(UserSession.session_id != except_session_id)
            
            sessions = query.all()
            count = 0
            
            for session in sessions:
                session.revoke("All sessions terminated")
                count += 1
            
            if count > 0:
                self.db.commit()
            
            logger.info(f"Terminated {count} sessions for user {user_id}")
            return count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to terminate sessions for user {user_id}: {e}")
            return 0
    
    def get_user_sessions(self, user_id: str, active_only: bool = True) -> List[UserSession]:
        """
        Get all sessions for a user.
        
        Args:
            user_id: The user's UUID
            active_only: If True, only return active sessions
            
        Returns:
            List of UserSession objects
        """
        query = self.db.query(UserSession).filter(UserSession.user_id == user_id)
        
        if active_only:
            query = query.filter(
                and_(
                    UserSession.status == SessionStatus.ACTIVE,
                    UserSession.expires_at > datetime.utcnow()
                )
            )
        
        return query.order_by(UserSession.last_activity_at.desc()).all()
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions (maintenance task).
        
        Returns:
            Number of sessions cleaned up
        """
        try:
            expired_sessions = self.db.query(UserSession).filter(
                and_(
                    UserSession.status == SessionStatus.ACTIVE,
                    UserSession.expires_at <= datetime.utcnow()
                )
            ).all()
            
            count = 0
            for session in expired_sessions:
                session.expire()
                count += 1
            
            if count > 0:
                self.db.commit()
            
            logger.info(f"Cleaned up {count} expired sessions")
            return count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to cleanup expired sessions: {e}")
            return 0
    
    def _terminate_session(self, session: UserSession, reason: str):
        """Internal method to terminate a session."""
        session.revoke(reason)
        self.db.commit()
        logger.info(f"Terminated session {session.session_id}: {reason}")
    
    def _hash_token(self, token: str) -> str:
        """Hash a token for secure storage."""
        return hashlib.sha256(token.encode()).hexdigest()
