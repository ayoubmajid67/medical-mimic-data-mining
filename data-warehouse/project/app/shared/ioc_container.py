"""Dependency Injection Container for shared resources."""
from typing import Generator

from sqlalchemy.orm import Session

from .config import Settings, settings
from .db_engine import SessionLocal, engine
from .logger import logger, setup_logger


class Container:
    """IoC Container for dependency injection."""

    def __init__(self):
        """Initialize container with default instances."""
        self._settings = settings
        self._logger = logger
        self._engine = engine

    @property
    def config(self) -> Settings:
        """Get application settings."""
        return self._settings

    @property
    def log(self):
        """Get logger instance."""
        return self._logger

    def get_db(self) -> Generator[Session, None, None]:
        """
        Get database session.

        Yields:
            SQLAlchemy Session
        """
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            self._logger.error(f"Session error: {e}")
            raise
        finally:
            session.close()

    def get_new_logger(self, name: str):
        """
        Create a new logger with specific name.

        Args:
            name: Logger name

        Returns:
            Logger instance
        """
        return setup_logger(name)


# Global container instance
container = Container()
