#!/usr/bin/env python3
"""
Database initialization script for MartechEngine.
This script creates all database tables based on the SQLAlchemy models.
"""

import logging
from app.core.database import engine
from app.models import Base

def init_db():
    """Create all database tables based on the SQLAlchemy models."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    init_db()
