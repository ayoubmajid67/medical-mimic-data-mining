"""ICU stay transformer: Bronze → Silver."""
from typing import Dict, Any, Optional
from datetime import datetime

from app.models.bronze import BronzeICUStays
from app.models.silver import SilverICUStay
from .base_transformer import BaseSilverTransformer


class ICUStayTransformer(BaseSilverTransformer):
    """Transform ICU stay data from Bronze to Silver layer."""
    
    @property
    def bronze_model(self):
        return BronzeICUStays
    
    @property
    def silver_model(self):
        return SilverICUStay
    
    def calculate_icu_los(self, intime: datetime, outtime: Optional[datetime]) -> tuple:
        """
        Calculate ICU length of stay.
        
        Args:
            intime: ICU admission time
            outtime: ICU discharge time
            
        Returns:
            Tuple of (los_icu_days, los_icu_hours)
        """
        if not outtime or not intime:
            return None, None
        
        delta = outtime - intime
        los_hours = delta.total_seconds() / 3600
        los_days = los_hours / 24
        
        return round(los_days, 2), round(los_hours, 2)
    
    def transform_record(self, bronze: BronzeICUStays) -> Dict[str, Any]:
        """
        Transform bronze ICU stay to silver format.
        
        Transformations:
        - Calculate ICU length of stay
        - Standardize care unit names
        """
        los_days, los_hours = self.calculate_icu_los(bronze.intime, bronze.outtime)
        
        return {
            "icustay_id": bronze.icustay_id,
            "subject_id": bronze.subject_id,
            "hadm_id": bronze.hadm_id,
            "first_careunit": bronze.first_careunit,
            "last_careunit": bronze.last_careunit,
            "first_wardid": bronze.first_wardid,
            "last_wardid": bronze.last_wardid,
            "intime": bronze.intime,
            "outtime": bronze.outtime,
            "los_icu_days": los_days,
            "los_icu_hours": los_hours,
        }
