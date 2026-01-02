"""Performance monitoring for data loading."""
import sys
import time
from pathlib import Path
from typing import Dict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.shared import get_db, logger, settings
from app.transformers.bronze import load_table


def benchmark_table_load(table_name: str, csv_dir: Path, batch_sizes: list[int]) -> Dict:
    """
    Benchmark loading performance with different batch sizes.
    
    Args:
        table_name: Name of table to benchmark
        csv_dir: Directory containing CSV files
        batch_sizes: List of batch sizes to test
        
    Returns:
        Performance statistics
    """
    results = {}
    
    logger.info(f"Benchmarking {table_name} with batch sizes: {batch_sizes}")
    
    for batch_size in batch_sizes:
        logger.info(f"\nTesting batch size: {batch_size}")
        
        start_time = time.time()
        
        try:
            with get_db() as session:
                stats = load_table(session, table_name, csv_dir, batch_size)
            
            duration = time.time() - start_time
            rows_per_sec = stats['loaded'] / duration if duration > 0 else 0
            
            results[batch_size] = {
                'duration': duration,
                'rows_loaded': stats['loaded'],
                'rows_per_second': rows_per_sec,
                'errors': stats['errors'],
            }
            
            logger.info(f"Duration: {duration:.2f}s")
            logger.info(f"Rows/sec: {rows_per_sec:.2f}")
            
        except Exception as e:
            logger.error(f"Failed with batch size {batch_size}: {e}")
            results[batch_size] = {'error': str(e)}
    
    return results


def main():
    """Run benchmark tests."""
    # Test with CAREGIVERS (small table) first
    table_name = "CAREGIVERS"
    csv_dir = settings.csv_data_path
    batch_sizes = [100, 500, 1000, 5000]
    
    logger.info("=== Bronze Layer Performance Benchmark ===\n")
    
    results = benchmark_table_load(table_name, csv_dir, batch_sizes)
    
    # Print summary
    logger.info("\n=== Benchmark Results ===")
    logger.info(f"Table: {table_name}")
    
    for batch_size, stats in results.items():
        if 'error' not in stats:
            logger.info(
                f"\nBatch Size {batch_size}: "
                f"{stats['duration']:.2f}s, "
                f"{stats['rows_per_second']:.2f} rows/sec"
            )
    
    # Find optimal batch size
    valid_results = {k: v for k, v in results.items() if 'error' not in v}
    if valid_results:
        best_batch = max(valid_results.items(), key=lambda x: x[1]['rows_per_second'])
        logger.info(f"\nOptimal batch size: {best_batch[0]}")


if __name__ == "__main__":
    main()
