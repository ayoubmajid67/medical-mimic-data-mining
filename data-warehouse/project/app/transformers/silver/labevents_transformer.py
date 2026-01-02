"""Lab events transformer: Bronze → Silver."""
from typing import Dict, Any

from app.models.bronze import BronzeLabEvents
from app.models.silver import SilverLabEvent
from .base_transformer import BaseSilverTransformer


class LabEventsTransformer(BaseSilverTransformer):
    """Transform lab events data from Bronze to Silver layer."""
    
    @property
    def bronze_model(self):
        return BronzeLabEvents
    
    @property
    def silver_model(self):
        return SilverLabEvent
    
    def parse_numeric_value(self, value: str) -> float:
        """
        Parse numeric value from string.
        
        Handles cases like:
        - "5.5" → 5.5
        - ">10" → 10.0
        - "<0.5" → 0.5
        - "NEGATIVE" → None
        """
        if not value:
            return None
        
        value = value.strip()
        
        # Remove common prefixes
        for prefix in ['>', '<', '>=', '<=', '~']:
            if value.startswith(prefix):
                value = value[len(prefix):]
        
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def determine_abnormal(self, flag: str) -> bool:
        """
        Determine if result is abnormal based on flag.
        
        Args:
            flag: Flag value from bronze
            
        Returns:
            True if abnormal
        """
        if not flag:
            return False
        
        abnormal_flags = ['abnormal', 'delta', 'high', 'low', 'H', 'L', 'A']
        return flag.upper() in [f.upper() for f in abnormal_flags]
    
    def transform_record(self, bronze: BronzeLabEvents) -> Dict[str, Any]:
        """
        Transform bronze lab event to silver format.
        
        Transformations:
        - Parse numeric values
        - Determine abnormal flag
        - Standardize units
        """
        valuenum = bronze.valuenum
        if valuenum is None and bronze.value:
            valuenum = self.parse_numeric_value(bronze.value)
        
        is_abnormal = self.determine_abnormal(bronze.flag)
        
        return {
            "row_id": bronze.row_id,
            "subject_id": bronze.subject_id,
            "hadm_id": bronze.hadm_id,
            "itemid": bronze.itemid,
            "charttime": bronze.charttime,
            "value": bronze.value,
            "valuenum": valuenum,
            "valueuom": bronze.valueuom,
            "flag": bronze.flag,
            "is_abnormal": is_abnormal,
        }
