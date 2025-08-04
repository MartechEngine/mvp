from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any

T = TypeVar('T')

class APIErrorDetail(BaseModel):
    """Schema for API error details."""
    code: str
    message: str
    field: Optional[str] = None

class APIErrorResponse(BaseModel):
    """Schema for API error responses."""
    error: APIErrorDetail

class APISuccessResponse(BaseModel, Generic[T]):
    """Schema for successful API responses."""
    data: T
    message: Optional[str] = None

class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    page: int = 1
    per_page: int = 20
    
    def __post_init__(self):
        if self.page < 1:
            self.page = 1
        if self.per_page < 1 or self.per_page > 100:
            self.per_page = 20

class PaginatedResponse(BaseModel, Generic[T]):
    """Schema for paginated API responses."""
    items: list[T]
    total: int
    page: int
    per_page: int
    pages: int
