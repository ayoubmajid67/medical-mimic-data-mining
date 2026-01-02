"""Quick query examples for Bronze layer."""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.bronze import BronzeAdmissions, BronzePatients
from app.shared import get_db, logger


def example_count_patients():
    """Count total patients."""
    with next(get_db()) as db:
        count = db.query(BronzePatients).count()
        logger.info(f"Total patients: {count}")
        return count


def example_get_first_patients(limit=5):
    """Get first N patients."""
    with next(get_db()) as db:
        patients = db.query(BronzePatients).limit(limit).all()
        
        logger.info(f"\nFirst {limit} patients:")
        for p in patients:
            logger.info(
                f"  Patient {p.subject_id}: {p.gender}, "
                f"Born {p.dob.strftime('%Y-%m-%d')}, "
                f"Expired: {p.expire_flag}"
            )
        
        return patients


def example_count_admissions():
    """Count total admissions."""
    with next(get_db()) as db:
        count = db.query(BronzeAdmissions).count()
        logger.info(f"\nTotal admissions: {count}")
        return count


def example_emergency_admissions(limit=5):
    """Get emergency admissions."""
    with next(get_db()) as db:
        admissions = (
            db.query(BronzeAdmissions)
            .filter(BronzeAdmissions.admission_type == "EMERGENCY")
            .limit(limit)
            .all()
        )
        
        logger.info(f"\nFirst {limit} emergency admissions:")
        for adm in admissions:
            logger.info(
                f"  Admission {adm.hadm_id}: Patient {adm.subject_id}, "
                f"Diagnosis: {adm.diagnosis}, "
                f"Expired: {adm.hospital_expire_flag}"
            )
        
        return admissions


def example_join_patients_admissions(limit=5):
    """Join patients and admissions."""
    with next(get_db()) as db:
        results = (
            db.query(BronzePatients, BronzeAdmissions)
            .join(
                BronzeAdmissions,
                BronzePatients.subject_id == BronzeAdmissions.subject_id
            )
            .limit(limit)
            .all()
        )
        
        logger.info(f"\nFirst {limit} patient-admission pairs:")
        for patient, admission in results:
            logger.info(
                f"  Patient {patient.subject_id} ({patient.gender}): "
                f"Admission {admission.hadm_id} - {admission.diagnosis}"
            )
        
        return results


def main():
    """Run example queries."""
    logger.info("=== Bronze Layer Query Examples ===\n")
    
    try:
        # Run examples
        example_count_patients()
        example_get_first_patients()
        example_count_admissions()
        example_emergency_admissions()
        example_join_patients_admissions()
        
        logger.info("\n✓ All example queries completed successfully")
        
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
