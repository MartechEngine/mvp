class AppError(Exception):
    """Base class for application-specific errors."""
    pass

class EmailAlreadyExistsError(AppError):
    """Raised when a user tries to register with an email that already exists."""
    pass

class InvalidCredentialsError(AppError):
    """Raised when a login attempt fails due to incorrect email or password."""
    pass

class InsufficientCreditsError(AppError):
    """Raised when an operation requires more credits than available."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    pass

class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
    pass

class PermissionDeniedError(AppError):
    """Raised when a user lacks permission for an operation."""
    pass
    """Base class for application-specific errors."""
    pass

class EmailAlreadyExistsError(AppError):
    """Raised when a user tries to register with an email that already exists."""
    pass

class InvalidCredentialsError(AppError):
    """Raised when a login attempt fails due to incorrect email or password."""
    pass

class InsufficientCreditsError(AppError):
    """Raised when an operation requires more credits than available."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    pass

class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
    pass

class PermissionDeniedError(AppError):
    """Raised when a user lacks permission for an operation."""
    pass
