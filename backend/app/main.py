import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.exception_handlers import setup_exception_handlers
from app.api.v1.endpoints import auth

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# Set up CORS middleware - Always allow localhost:3000 for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers
setup_exception_handlers(app)

# Include API routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to ensure the API is running."""
    return {"status": "ok"}

@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint with a welcome message."""
    return {"message": f"Welcome to the {settings.PROJECT_NAME} API"}