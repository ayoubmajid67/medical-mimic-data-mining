"""Output events transformer: Bronze → Silver."""
from typing import Dict, Any

from app.models.bronze import BronzeOutputEvents
from app.models.silver import SilverOutputEvent
from .base_transformer import BaseSilverTransformer


class OutputEventsTransformer(BaseSilverTransformer):
    """Transform output events data from Bronze to Silver layer."""
    
    @property
    def bronze_model(self):
        return BronzeOutputEvents
    
    @property
    def silver_model(self):
        return SilverOutputEvent
    
    def transform_record(self, bronze: BronzeOutputEvents) -> Dict[str, Any]:
        """Transform bronze output event to silver format."""
        return {
            "row_id": bronze.row_id,
            "subject_id": bronze.subject_id,
            "hadm_id": bronze.hadm_id,
            "icustay_id": bronze.icustay_id,
            "itemid": bronze.itemid,
            "charttime": bronze.charttime,
            "value": bronze.value,
            "valueuom": bronze.valueuom,
            "cgid": bronze.cgid,
        }
