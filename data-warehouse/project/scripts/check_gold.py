"""Check Gold layer table counts."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.shared import get_db

def main():
    with get_db() as s:
        tables = [
            'dim_patient', 'dim_time', 'dim_careunit', 'dim_item', 'dim_labitem',
            'dim_service', 'dim_procedure_icd', 'dim_caregiver',
            'fact_admission', 'fact_icu_stay', 'fact_lab_event', 'fact_prescription',
            'fact_transfer', 'fact_input_event', 'fact_output_event', 'fact_procedure', 'fact_microbiology',
            'agg_patient_summary', 'agg_daily_census', 'agg_icu_performance',
            'agg_lab_summary', 'agg_medication_usage', 'agg_infection_stats'
        ]
        print('Gold Layer Table Counts:')
        print('='*50)
        empty = []
        for t in tables:
            try:
                count = s.execute(text(f'SELECT COUNT(*) FROM gold.{t}')).scalar()
                status = '' if count > 0 else ' <- EMPTY'
                print(f'{t:30} {count:>8}{status}')
                if count == 0:
                    empty.append(t)
            except Exception as e:
                print(f'{t:30} ERROR: {e}')
        
        print('='*50)
        if empty:
            print(f'\nEmpty tables: {len(empty)}')
            for t in empty:
                print(f'  - {t}')
        else:
            print('\nAll tables have data!')
    return 0

if __name__ == "__main__":
    sys.exit(main())
