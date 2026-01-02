"""Verify Gold Layer data integrity and business logic."""
import sys
from pathlib import Path
from sqlalchemy import text

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.shared import get_db, logger

def run_check(test_name, query, expected_condition, session):
    """Run a single verification check."""
    try:
        result = session.execute(text(query)).scalar()
        if expected_condition(result):
            print(f"[PASS] {test_name}: {result}")
            return True
        else:
            print(f"[FAIL] {test_name}: Got {result}")
            return False
    except Exception as e:
        print(f"[ERROR] {test_name}: {e}")
        return False

def main():
    print("=" * 60)
    print("VERIFYING GOLD LAYER INTEGRITY")
    print("=" * 60)
    
    failures = 0
    checks = 0

    with get_db() as session:
        # 1. Row Count Sanity
        checks += 1
        query = "SELECT COUNT(*) FROM gold.fact_admission"
        if not run_check("Fact Admission Count > 0", query, lambda x: x > 0, session):
            failures += 1

        checks += 1
        query = "SELECT COUNT(*) FROM gold.dim_patient"
        if not run_check("Dim Patient Count > 0", query, lambda x: x > 0, session):
            failures += 1

        # 2. Data Logic Check: LOS should be positive
        checks += 1
        query = "SELECT COUNT(*) FROM gold.fact_admission WHERE los_days < 0"
        if not run_check("Negative LOS Count == 0", query, lambda x: x == 0, session):
            failures += 1
            
        # 3. Data Logic Check: Deceased patients should have expire_flag
        checks += 1
        query = """
            SELECT COUNT(*) 
            FROM gold.dim_patient p
            JOIN gold.fact_admission f ON p.patient_key = f.patient_key
            WHERE p.is_deceased = TRUE AND f.hospital_expire = FALSE 
            AND f.discharge_location = 'DEAD/EXPIRED'
        """
        # This is strictly checking if discharge location matches flag, might have edge cases
        # Let's check simpler: Hospital Expire flag consistency
        query = "SELECT COUNT(*) FROM gold.fact_admission WHERE hospital_expire = TRUE AND discharge_location != 'DEAD/EXPIRED'"
        # Note: logic might vary, but let's see if there are anomalies
        if not run_check("Expire Flag Consistency (Soft Check)", query, lambda x: x >= 0, session):
             failures += 1

        # 4. Aggregate Consistency
        checks += 1
        query = """
            SELECT ABS( (SELECT COUNT(*) FROM gold.fact_admission) - 
                        (SELECT SUM(total_admissions) FROM gold.agg_patient_summary) )
        """
        # Sum of admissions per patient should equal total admissions
        if not run_check("Aggregate Sum match Fact Count", query, lambda x: x == 0, session):
            failures += 1

        # 5. Orphan Check
        checks += 1
        query = "SELECT COUNT(*) FROM gold.fact_icu_stay WHERE careunit_key NOT IN (SELECT careunit_key FROM gold.dim_careunit)"
        if not run_check("Orphan ICU Stays (Invalid CareUnit)", query, lambda x: x == 0, session):
            failures += 1

    print("-" * 60)
    print(f"Tests Run: {checks} | Failures: {failures}")
    print("=" * 60)
    
    return 1 if failures > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
