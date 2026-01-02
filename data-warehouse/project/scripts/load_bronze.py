"""Load CSV data into Bronze tables."""
import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.shared import get_db, logger, settings
from app.transformers.bronze import load_all_tables, load_table


def main():
    """Main entry point for data loading."""
    parser = argparse.ArgumentParser(description="Load MIMIC-III CSV data into Bronze tables")
    parser.add_argument(
        "--table",
        type=str,
        help="Specific table  to load (e.g., PATIENTS). If not specified, loads all tables.",
    )
    parser.add_argument(
        "--csv-dir",
        type=Path,
        default=settings.csv_data_path,
        help=f"Directory containing CSV files (default: {settings.csv_data_path})",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=settings.batch_size,
        help=f"Batch size for loading (default: {settings.batch_size})",
    )

    args = parser.parse_args()

    # Validate CSV directory
    if not args.csv_dir.exists():
        logger.error(f"CSV directory not found: {args.csv_dir}")
        sys.exit(1)

    logger.info(f"CSV directory: {args.csv_dir}")
    logger.info(f"Batch size: {args.batch_size}")

    try:
        with get_db() as session:
            if args.table:
                # Load specific table
                logger.info(f"Loading table: {args.table}")
                stats = load_table(session, args.table, args.csv_dir, args.batch_size)
                
                print("\n=== Loading Statistics ===")
                print(f"Table: {args.table}")
                print(f"Total rows: {stats['total']}")
                print(f"Loaded: {stats['loaded']}")
                print(f"Errors: {stats['errors']}")
            else:
                # Load all tables
                logger.info("Loading all tables...")
                all_stats = load_all_tables(session, args.csv_dir, args.batch_size)
                
                print("\n=== Loading Statistics ===")
                for table_name, stats in all_stats.items():
                    if "error" in stats:
                        print(f"\n{table_name}: ERROR - {stats['error']}")
                    else:
                        print(f"\n{table_name}:")
                        print(f"  Total rows: {stats['total']}")
                        print(f"  Loaded: {stats['loaded']}")
                        print(f"  Errors: {stats['errors']}")

        logger.info("Data loading completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Data loading failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
