"""SQLAlchemy database engine and session management."""
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from .config import settings
from .logger import logger

# Create SQLAlchemy engine
engine: Engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=True,  # Verify connections before using
    echo=not settings.is_production,  # Log SQL in development
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Connection event listeners
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Handle new database connections."""
    logger.debug("New database connection established")


@event.listens_for(engine, "close")
def receive_close(dbapi_conn, connection_record):
    """Handle database connection closures."""
    logger.debug("Database connection closed")


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session with automatic cleanup.

    Yields:
        SQLAlchemy Session

    Example:
        with get_db() as db:
            db.query(Patient).all()
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def dispose_engine():
    """Dispose of the engine and close all connections."""
    logger.info("Disposing database engine")
    engine.dispose()


def test_connection() -> bool:
    """
    Test database connection.

    Returns:
        True if connection successful, False otherwise
    """
    try:
        from sqlalchemy import text
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
