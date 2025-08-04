from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import EmailAlreadyExistsError, InvalidCredentialsError
from app.schemas.common_schemas import APIErrorResponse, APIErrorDetail

def setup_exception_handlers(app):
    @app.exception_handler(EmailAlreadyExistsError)
    async def email_already_exists_handler(request: Request, exc: EmailAlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=APIErrorResponse(
                error=APIErrorDetail(
                    code="AUTH_EMAIL_EXISTS",
                    message=str(exc)
                )
            ).model_dump()
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=APIErrorResponse(
                error=APIErrorDetail(
                    code="AUTH_INVALID_CREDENTIALS",
                    message=str(exc)
                )
            ).model_dump(),
            headers={"WWW-Authenticate": "Bearer"},
        )
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    EmailAlreadyExistsError, 
    InvalidCredentialsError,
    NotFoundError,
    ValidationError,
    PermissionDeniedError,
    InsufficientCreditsError
)
from app.schemas.common_schemas import APIErrorResponse, APIErrorDetail


def setup_exception_handlers(app):
    """Register custom exception handlers with the FastAPI application."""
    
    @app.exception_handler(EmailAlreadyExistsError)
    async def email_already_exists_handler(request: Request, exc: EmailAlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=APIErrorResponse(
                error=APIErrorDetail(
                    code="AUTH_EMAIL_EXISTS",
                    message=str(exc)
                )
            ).dict()
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=APIErrorResponse(
                error=APIErrorDetail(
                    code="AUTH_INVALID_CREDENTIALS",
                    message=str(exc)
                )
            ).dict(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=APIErrorResponse(
                error=APIErrorDetail(
                    code="RESOURCE_NOT_FOUND",
                    message=str(exc)
                )
            ).dict()
        )
    
    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIErrorResponse(
                error=APIErrorDetail(
                    code="VALIDATION_ERROR",
                    message=str(exc)
                )
            ).dict()
        )
    
    @app.exception_handler(PermissionDeniedError)
    async def permission_denied_handler(request: Request, exc: PermissionDeniedError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=APIErrorResponse(
                error=APIErrorDetail(
                    code="PERMISSION_DENIED",
                    message=str(exc)
                )
            ).dict()
        )
    
    @app.exception_handler(InsufficientCreditsError)
    async def insufficient_credits_handler(request: Request, exc: InsufficientCreditsError):
        return JSONResponse(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            content=APIErrorResponse(
                error=APIErrorDetail(
                    code="INSUFFICIENT_CREDITS",
                    message=str(exc)
                )
            ).model_dump()
        )
