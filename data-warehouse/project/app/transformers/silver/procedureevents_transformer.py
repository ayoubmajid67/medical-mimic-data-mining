"""Procedure events transformer: Bronze → Silver."""
from typing import Dict, Any, Optional
from datetime import datetime

from app.models.bronze import BronzeProcedureEventsMetaVision
from app.models.silver import SilverProcedureEvent
from .base_transformer import BaseSilverTransformer


class ProcedureEventsTransformer(BaseSilverTransformer):
    """Transform procedure events data from Bronze to Silver layer."""
    
    @property
    def bronze_model(self):
        return BronzeProcedureEventsMetaVision
    
    @property
    def silver_model(self):
        return SilverProcedureEvent
    
    def calculate_duration(self, start: datetime, end: datetime) -> Optional[float]:
        """Calculate duration in hours."""
        if not start or not end:
            return None
        delta = end - start
        return round(delta.total_seconds() / 3600, 2)
    
    def transform_record(self, bronze: BronzeProcedureEventsMetaVision) -> Dict[str, Any]:
        """Transform bronze procedure event to silver format."""
        duration = self.calculate_duration(bronze.starttime, bronze.endtime)
        
        # Determine status flags
        status = bronze.statusdescription.upper() if bronze.statusdescription else ""
        is_canceled = "CANCEL" in status
        is_completed = not is_canceled and bronze.endtime is not None
        
        return {
            "row_id": bronze.row_id,
            "subject_id": bronze.subject_id,
            "hadm_id": bronze.hadm_id,
            "icustay_id": bronze.icustay_id,
            "itemid": bronze.itemid,
            "starttime": bronze.starttime,
            "endtime": bronze.endtime,
            "value": bronze.value,
            "valueuom": bronze.valueuom,
            "location": bronze.location,
            "status_description": bronze.statusdescription,
            "is_completed": is_completed,
            "is_canceled": is_canceled,
            "duration_hours": duration,
        }
