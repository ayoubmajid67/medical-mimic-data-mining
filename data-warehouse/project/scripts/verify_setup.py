"""Quick verification script to test Bronze layer setup."""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.bronze import (
    BronzeAdmissions,
    BronzeCaregivers,
    BronzeDItems,
    BronzeDLabItems,
    BronzeICUStays,
    BronzeInputEventsCareVue,
    BronzeInputEventsMetaVision,
    BronzeLabEvents,
    BronzeMicrobiologyEvents,
    BronzeNoteEvents,
    BronzeOutputEvents,
    BronzePatients,
    BronzePrescriptions,
    BronzeProcedureEventsMetaVision,
    BronzeServices,
    BronzeTransfers,
)
from app.shared import logger, settings, test_connection


def verify_config():
    """Verify configuration is loaded correctly."""
    logger.info("=== Configuration Check ===")
    logger.info(f"Database URL: {settings.database_url}")
    logger.info(f"CSV Path: {settings.csv_data_path}")
    logger.info(f"Batch Size: {settings.batch_size}")
    logger.info(f"Environment: {settings.env}")
    return True


def verify_models():
    """Verify all models are importable."""
    logger.info("=== Models Check ===")
    models = [
        BronzePatients,
        BronzeAdmissions,
        BronzeICUStays,
        BronzeCaregivers,
        BronzeServices,
        BronzeTransfers,
        BronzeDItems,
        BronzeDLabItems,
        BronzeLabEvents,
        BronzeInputEventsCareVue,
        BronzeInputEventsMetaVision,
        BronzeOutputEvents,
        BronzePrescriptions,
        BronzeProcedureEventsMetaVision,
        BronzeMicrobiologyEvents,
        BronzeNoteEvents,
    ]
    
    logger.info(f"Total models defined: {len(models)}")
    for model in models:
        logger.info(f"  ✓ {model.__tablename__}")
    
    return True


def verify_database():
    """Verify database connection."""
    logger.info("=== Database Connection Check ===")
    if test_connection():
        logger.info("✓ Database connection successful")
        return True
    else:
        logger.error("✗ Database connection failed")
        return False


def verify_tables():
    """Verify tables exist in database."""
    logger.info("=== Database Tables Check ===")
    try:
        from sqlalchemy import inspect
        from app.shared import engine
        
        inspector = inspect(engine)
        tables = inspector.get_table_names(schema="bronze")
        
        if tables:
            logger.info(f"Found {len(tables)} tables in bronze schema:")
            for table in sorted(tables):
                logger.info(f"  ✓ {table}")
            return True
        else:
            logger.warning("No tables found. Run 'python scripts/init_db.py' first.")
            return False
            
    except Exception as e:
        logger.error(f"Error checking tables: {e}")
        return False


def main():
    """Run all verification checks."""
    logger.info("Starting Bronze Layer Verification...\n")
    
    checks = [
        ("Configuration", verify_config),
        ("Models Import", verify_models),
        ("Database Connection", verify_database),
        ("Database Tables", verify_tables),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
            logger.info("")  # Blank line
        except Exception as e:
            logger.error(f"{check_name} failed with error: {e}")
            results.append((check_name, False))
            logger.info("")
    
    # Summary
    logger.info("=== Verification Summary ===")
    all_passed = all(result for _, result in results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {check_name}")
    
    if all_passed:
        logger.info("\n🎉 All checks passed! Bronze layer is ready.")
        return 0
    else:
        logger.warning("\n⚠️  Some checks failed. Review the logs above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
