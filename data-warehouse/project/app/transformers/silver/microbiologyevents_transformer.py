"""Microbiology events transformer: Bronze → Silver."""
from typing import Dict, Any

from app.models.bronze import BronzeMicrobiologyEvents
from app.models.silver import SilverMicrobiologyEvent
from .base_transformer import BaseSilverTransformer


class MicrobiologyEventsTransformer(BaseSilverTransformer):
    """Transform microbiology events data from Bronze to Silver layer."""
    
    @property
    def bronze_model(self):
        return BronzeMicrobiologyEvents
    
    @property
    def silver_model(self):
        return SilverMicrobiologyEvent
    
    def transform_record(self, bronze: BronzeMicrobiologyEvents) -> Dict[str, Any]:
        """Transform bronze microbiology event to silver format."""
        # Positive culture if organism was found
        is_positive = bronze.org_name is not None and bronze.org_name.strip() != ""
        
        # Resistant if interpretation is 'R'
        interpretation = bronze.interpretation.upper() if bronze.interpretation else ""
        is_resistant = interpretation == "R"
        
        return {
            "row_id": bronze.row_id,
            "subject_id": bronze.subject_id,
            "hadm_id": bronze.hadm_id,
            "chartdate": bronze.chartdate,
            "charttime": bronze.charttime,
            "spec_itemid": bronze.spec_itemid,
            "spec_type_desc": bronze.spec_type_desc,
            "org_itemid": bronze.org_itemid,
            "org_name": bronze.org_name,
            "ab_itemid": bronze.ab_itemid,
            "ab_name": bronze.ab_name,
            "dilution_text": bronze.dilution_text,
            "interpretation": bronze.interpretation,
            "is_positive": is_positive,
            "is_resistant": is_resistant,
        }
