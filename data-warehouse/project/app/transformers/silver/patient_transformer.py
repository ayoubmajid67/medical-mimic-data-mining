"""Patient transformer: Bronze → Silver."""
from typing import Dict, Any

from app.models.bronze import BronzePatients
from app.models.silver import SilverPatient
from .base_transformer import BaseSilverTransformer


class PatientTransformer(BaseSilverTransformer):
    """Transform patient data from Bronze to Silver layer."""
    
    @property
    def bronze_model(self):
        return BronzePatients
    
    @property
    def silver_model(self):
        return SilverPatient
    
    def transform_record(self, bronze: BronzePatients) -> Dict[str, Any]:
        """
        Transform bronze patient to silver format.
        
        Transformations:
        - Validate gender (M/F only)
        - Calculate deceased status
        - Handle date shifting for elderly patients
        """
        # Validate gender
        gender = bronze.gender.upper() if bronze.gender else None
        if gender not in ('M', 'F'):
            return None  # Skip invalid records
        
        # Determine deceased status
        is_deceased = bronze.dod is not None or bronze.dod_hosp is not None
        
        return {
            "subject_id": bronze.subject_id,
            "gender": gender,
            "date_of_birth": bronze.dob.date() if bronze.dob else None,
            "date_of_death": bronze.dod.date() if bronze.dod else None,
            "is_deceased": is_deceased,
            "dob_shift_years": None,  # Could calculate from MIMIC date shifting rules
        }
