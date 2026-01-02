"""Refresh Gold layer aggregate tables."""
import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.shared import get_db, logger
# Import aggregate loaders from load_gold script
# Note: This assumes load_gold.py is in the same directory and accessible
try:
    from scripts.load_gold import (
        create_gold_schema,
        load_agg_patient_summary,
        load_agg_icu_performance,
        load_agg_daily_census,
        load_agg_lab_summary,
        load_agg_medication_usage,
        load_agg_infection_stats
    )
except ImportError:
    # Fallback if running as script vs module
    from load_gold import (
        create_gold_schema,
        load_agg_patient_summary,
        load_agg_icu_performance,
        load_agg_daily_census,
        load_agg_lab_summary,
        load_agg_medication_usage,
        load_agg_infection_stats
    )

def main():
    parser = argparse.ArgumentParser(description="Refresh Gold Layer Aggregates")
    parser.parse_args()

    logger.info("=" * 60)
    logger.info("REFRESHING GOLD AGGREGATES")
    logger.info("=" * 60)

    try:
        with get_db() as session:
            # Ensure schema exists
            create_gold_schema(session)

            # Reload all aggregates
            logger.info("\n--- Refreshing Patient Summary ---")
            load_agg_patient_summary(session)

            logger.info("\n--- Refreshing ICU Performance ---")
            load_agg_icu_performance(session)

            logger.info("\n--- Refreshing Daily Census ---")
            load_agg_daily_census(session)

            logger.info("\n--- Refreshing Lab Summary ---")
            load_agg_lab_summary(session)

            logger.info("\n--- Refreshing Medication Usage ---")
            load_agg_medication_usage(session)
            
            logger.info("\n--- Refreshing Infection Stats ---")
            load_agg_infection_stats(session)

            logger.info("\n" + "=" * 60)
            logger.info("Aggregate refresh complete!")
            logger.info("=" * 60)
        
        return 0

    except Exception as e:
        logger.error(f"Aggregate refresh failed: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
