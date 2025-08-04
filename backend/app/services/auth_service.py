from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.models.organization import Organization
from app.schemas.user_schemas import UserCreate

class AuthService:
    async def get_user_by_email(self, db: AsyncSession, *, email: str) -> User | None:
        """Asynchronously get a user by email."""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def register(self, db: AsyncSession, *, user_create: UserCreate) -> User:
        """Asynchronously register a new user and create their organization."""
        # Create the user first
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            full_name=user_create.full_name,
            email=user_create.email,
            hashed_password=hashed_password,
            organization_id=None,  # Will be set after creating organization
            is_active=True,  # Defaulting to active, can be changed for email verification
        )
        db.add(db_user)
        await db.flush()  # Flush to get the user's ID

        # Create the organization with the user as owner
        new_org = Organization(
            name=user_create.organization_name,
            owner_id=db_user.id
        )
        db.add(new_org)
        await db.flush()  # Flush to get the organization's ID

        # Update the user's organization_id
        db_user.organization_id = new_org.id
        
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> User | None:
        """Asynchronously authenticate a user."""
        user = await self.get_user_by_email(db, email=email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

        if user.is_verified:
            logger.info(f"Resend verification attempted for already verified user: {email}")
            raise ValidationError("This email address is already verified.")
        
        # TODO: Implement email verification token generation and sending
        # This will be completed when EmailService and EmailVerificationToken are implemented
        logger.info(f"Verification email resend requested for: {email}")
        return True
