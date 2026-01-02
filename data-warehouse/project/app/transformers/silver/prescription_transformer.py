"""Prescription transformer: Bronze → Silver."""
from typing import Dict, Any, Optional
from datetime import datetime

from app.models.bronze import BronzePrescriptions
from app.models.silver import SilverPrescription
from .base_transformer import BaseSilverTransformer


class PrescriptionTransformer(BaseSilverTransformer):
    """Transform prescription data from Bronze to Silver layer."""
    
    @property
    def bronze_model(self):
        return BronzePrescriptions
    
    @property
    def silver_model(self):
        return SilverPrescription
    
    def parse_dose_value(self, value: str) -> Optional[float]:
        """Parse dose value from string."""
        if not value:
            return None
        try:
            # Remove common prefixes/suffixes
            cleaned = value.strip().replace(',', '')
            return float(cleaned)
        except (ValueError, TypeError):
            return None
    
    def calculate_duration(self, start: datetime, end: datetime) -> Optional[float]:
        """Calculate duration in days."""
        if not start or not end:
            return None
        delta = end - start
        return round(delta.total_seconds() / 86400, 2)
    
    def transform_record(self, bronze: BronzePrescriptions) -> Dict[str, Any]:
        """Transform bronze prescription to silver format."""
        duration = self.calculate_duration(bronze.startdate, bronze.enddate)
        
        return {
            "row_id": bronze.row_id,
            "subject_id": bronze.subject_id,
            "hadm_id": bronze.hadm_id,
            "icustay_id": bronze.icustay_id,
            "startdate": bronze.startdate,
            "enddate": bronze.enddate,
            "drug_type": bronze.drug_type,
            "drug": bronze.drug,
            "drug_name_generic": bronze.drug_name_generic,
            "formulary_drug_cd": bronze.formulary_drug_cd,
            "dose_val_rx": self.parse_dose_value(bronze.dose_val_rx),
            "dose_unit_rx": bronze.dose_unit_rx,
            "form_val_disp": self.parse_dose_value(bronze.form_val_disp),
            "form_unit_disp": bronze.form_unit_disp,
            "route": bronze.route,
            "duration_days": duration,
        }
