"""Initialize database schema - create all Bronze tables."""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.bronze import Base
from app.shared import db_engine, logger, settings


def init_db():
    """Create all Bronze layer tables in PostgreSQL."""
    logger.info("Initializing database schema...")
    logger.info(f"Database URL: {settings.database_url}")

    try:
        #Test connection first
        if not db_engine.test_connection():
            logger.error("Database connection failed. Is PostgreSQL running?")
            sys.exit(1)

        # Create bronze schema if it doesn't exist
        from sqlalchemy import text
        
        with db_engine.engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))
            conn.commit()
            logger.info("Created/verified 'bronze' schema")

        # Create all tables
        Base.metadata.create_all(bind=db_engine.engine)
        logger.info("Successfully created all Bronze tables")

        # List created tables
        from sqlalchemy import inspect

        inspector = inspect(db_engine.engine)
        tables = inspector.get_table_names(schema="bronze")
        logger.info(f"Tables in bronze schema: {len(tables)}")
        for table in sorted(tables):
            logger.info(f"  - {table}")

        return True

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False


if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)
