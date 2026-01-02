"""Drop and recreate gold schema."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.shared import get_db, logger

def main():
    logger.info("Dropping gold schema...")
    with get_db() as session:
        session.execute(text("DROP SCHEMA IF EXISTS gold CASCADE"))
        session.commit()
        logger.info("Gold schema dropped!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
