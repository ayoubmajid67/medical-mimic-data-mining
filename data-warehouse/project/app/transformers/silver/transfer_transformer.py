"""Transfer transformer: Bronze → Silver."""
from typing import Dict, Any, Optional
from datetime import datetime

from app.models.bronze import BronzeTransfers
from app.models.silver import SilverTransfer
from .base_transformer import BaseSilverTransformer


ICU_UNITS = ['MICU', 'SICU', 'CCU', 'CSRU', 'TSICU', 'NICU', 'NWARD']


class TransferTransformer(BaseSilverTransformer):
    """Transform transfer data from Bronze to Silver layer."""
    
    @property
    def bronze_model(self):
        return BronzeTransfers
    
    @property
    def silver_model(self):
        return SilverTransfer
    
    def calculate_duration(self, intime: datetime, outtime: datetime) -> Optional[float]:
        """Calculate duration in hours."""
        if not intime or not outtime:
            return None
        delta = outtime - intime
        return round(delta.total_seconds() / 3600, 2)
    
    def is_icu(self, careunit: str) -> bool:
        """Check if care unit is an ICU."""
        if not careunit:
            return False
        return careunit.upper() in ICU_UNITS
    
    def transform_record(self, bronze: BronzeTransfers) -> Dict[str, Any]:
        """Transform bronze transfer to silver format."""
        duration = self.calculate_duration(bronze.intime, bronze.outtime)
        is_icu = self.is_icu(bronze.curr_careunit) or self.is_icu(bronze.prev_careunit)
        
        return {
            "row_id": bronze.row_id,
            "subject_id": bronze.subject_id,
            "hadm_id": bronze.hadm_id,
            "icustay_id": bronze.icustay_id,
            "eventtype": bronze.eventtype,
            "prev_careunit": bronze.prev_careunit,
            "curr_careunit": bronze.curr_careunit,
            "prev_wardid": bronze.prev_wardid,
            "curr_wardid": bronze.curr_wardid,
            "intime": bronze.intime,
            "outtime": bronze.outtime,
            "duration_hours": duration,
            "is_icu_transfer": is_icu,
        }
