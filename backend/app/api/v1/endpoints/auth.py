from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.user_schemas import UserCreate, User
from app.schemas.auth_schemas import UserLogin
from app.schemas.token import Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
    auth_service: AuthService = Depends(AuthService)
) -> User:
    """
    Register a new user.
    """
    user = await auth_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    new_user = await auth_service.register(db=db, user_create=user_in)
    return new_user

@router.post("/login", response_model=Token)
async def login(
    *,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(AuthService),
    user_login: UserLogin
) -> Token:
    """
    Login with email and password, get an access token for future requests.
    """
    user = await auth_service.authenticate(
        db, email=user_login.email, password=user_login.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}
