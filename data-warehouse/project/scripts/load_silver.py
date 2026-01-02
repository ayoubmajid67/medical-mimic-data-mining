"""Transform Bronze data to Silver layer."""
import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.shared import get_db, logger
from app.models.silver import SilverBase
from app.transformers.silver import (
    PatientTransformer,
    AdmissionTransformer,
    ICUStayTransformer,
    CaregiverTransformer,
    LabEventsTransformer,
    PrescriptionTransformer,
    TransferTransformer,
    InputEventsTransformer,
    OutputEventsTransformer,
    ProcedureEventsTransformer,
    MicrobiologyEventsTransformer,
)


def create_silver_schema(session):
    """Create silver schema if it doesn't exist."""
    from sqlalchemy import text
    session.execute(text("CREATE SCHEMA IF NOT EXISTS silver"))
    session.commit()
    logger.info("Silver schema created/verified")


def create_silver_tables(engine):
    """Create silver layer tables."""
    SilverBase.metadata.create_all(engine)
    logger.info("Silver tables created")


# Standard transformers (use base class)
STANDARD_TRANSFORMERS = {
    "patients": PatientTransformer,
    "admissions": AdmissionTransformer,
    "icustays": ICUStayTransformer,
    "caregivers": CaregiverTransformer,
    "labevents": LabEventsTransformer,
    "prescriptions": PrescriptionTransformer,
    "transfers": TransferTransformer,
    "outputevents": OutputEventsTransformer,
    "procedureevents": ProcedureEventsTransformer,
    "microbiologyevents": MicrobiologyEventsTransformer,
}

# Special transformers (custom implementation)
SPECIAL_TRANSFORMERS = {
    "inputevents": InputEventsTransformer,  # Merges CV + MV
}

ALL_TABLES = list(STANDARD_TRANSFORMERS.keys()) + list(SPECIAL_TRANSFORMERS.keys())
# ALL_TABLES = list(STANDARD_TRANSFORMERS.keys()) + list(SPECIAL_TRANSFORMERS.keys())


def main():
    """Main entry point for silver layer transformation."""
    parser = argparse.ArgumentParser(description="Transform Bronze data to Silver layer")
    parser.add_argument(
        "--table",
        type=str,
        choices=ALL_TABLES,
        help="Specific table to transform. If not specified, transforms all tables.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Batch size for transformation (default: 1000)",
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("BRONZE → SILVER TRANSFORMATION")
    logger.info("=" * 60)
    
    try:
        with get_db() as session:
            # Create schema and tables
            create_silver_schema(session)
            create_silver_tables(session.get_bind())
            
            tables_to_transform = [args.table] if args.table else ALL_TABLES
            all_stats = {}
            
            for table_name in tables_to_transform:
                logger.info(f"\nTransforming: {table_name}")
                
                # Use appropriate transformer
                if table_name in STANDARD_TRANSFORMERS:
                    transformer_class = STANDARD_TRANSFORMERS[table_name]
                    transformer = transformer_class(session, batch_size=args.batch_size)
                else:
                    transformer_class = SPECIAL_TRANSFORMERS[table_name]
                    transformer = transformer_class(session, batch_size=args.batch_size)
                
                stats = transformer.transform()
                all_stats[table_name] = stats
            
            # Print summary
            print("\n" + "=" * 60)
            print("TRANSFORMATION SUMMARY")
            print("=" * 60)
            
            total_transformed = 0
            total_errors = 0
            
            for table_name, stats in all_stats.items():
                print(f"\n{table_name.upper()}:")
                print(f"  Total: {stats['total']}")
                print(f"  Transformed: {stats['transformed']}")
                print(f"  Errors: {stats['errors']}")
                total_transformed += stats['transformed']
                total_errors += stats['errors']
            
            print("\n" + "-" * 60)
            print(f"TOTAL: {total_transformed:,} records transformed, {total_errors} errors")
            
            logger.info("\nSilver layer transformation completed successfully")
            return 0
            
    except Exception as e:
        logger.error(f"Transformation failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
