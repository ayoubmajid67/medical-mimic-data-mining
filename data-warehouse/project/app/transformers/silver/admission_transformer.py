"""Admission transformer: Bronze → Silver."""
from typing import Dict, Any, Optional
from datetime import datetime

from app.models.bronze import BronzeAdmissions
from app.models.silver import SilverAdmission
from .base_transformer import BaseSilverTransformer


class AdmissionTransformer(BaseSilverTransformer):
    """Transform admission data from Bronze to Silver layer."""
    
    @property
    def bronze_model(self):
        return BronzeAdmissions
    
    @property
    def silver_model(self):
        return SilverAdmission
    
    def calculate_los(self, admittime: datetime, dischtime: Optional[datetime]) -> tuple:
        """
        Calculate length of stay in days and hours.
        
        Args:
            admittime: Admission timestamp
            dischtime: Discharge timestamp
            
        Returns:
            Tuple of (los_days, los_hours)
        """
        if not dischtime or not admittime:
            return None, None
        
        delta = dischtime - admittime
        los_hours = delta.total_seconds() / 3600
        los_days = los_hours / 24
        
        return round(los_days, 2), round(los_hours, 2)
    
    def transform_record(self, bronze: BronzeAdmissions) -> Dict[str, Any]:
        """
        Transform bronze admission to silver format.
        
        Transformations:
        - Calculate length of stay (days/hours)
        - Standardize admission types
        - Set mortality flag
        """
        # Calculate LOS
        los_days, los_hours = self.calculate_los(bronze.admittime, bronze.dischtime)
        
        # Mortality flag
        hospital_expire = bronze.hospital_expire_flag == 1 if bronze.hospital_expire_flag else False
        
        return {
            "hadm_id": bronze.hadm_id,
            "subject_id": bronze.subject_id,
            "admission_type": bronze.admission_type,
            "admission_location": bronze.admission_location,
            "discharge_location": bronze.discharge_location,
            "admittime": bronze.admittime,
            "dischtime": bronze.dischtime,
            "edregtime": bronze.edregtime,
            "edouttime": bronze.edouttime,
            "los_days": los_days,
            "los_hours": los_hours,
            "diagnosis": bronze.diagnosis,
            "hospital_expire_flag": hospital_expire,
            "insurance": bronze.insurance,
            "language": bronze.language,
            "religion": bronze.religion,
            "marital_status": bronze.marital_status,
            "ethnicity": bronze.ethnicity,
        }
