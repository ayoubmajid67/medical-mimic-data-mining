"""Caregiver transformer: Bronze → Silver."""
from typing import Dict, Any, Optional

from app.models.bronze import BronzeCaregivers
from app.models.silver import SilverCaregiver
from .base_transformer import BaseSilverTransformer


class CaregiverTransformer(BaseSilverTransformer):
    """Transform caregiver data from Bronze to Silver layer."""
    
    @property
    def bronze_model(self):
        return BronzeCaregivers
    
    @property
    def silver_model(self):
        return SilverCaregiver
    
    def _categorize_role(self, label: Optional[str]) -> Optional[str]:
        """
        Categorize caregiver role based on label code.
        
        Categories:
        - Nursing: RN, RN-BSN, RN-MSN, LPN, CNA
        - Physician: MD, DO, Res (Resident)
        - Respiratory: RT, RRT
        - Other: RO (Read Only), etc.
        """
        if not label:
            return None
            
        label_upper = label.upper().strip()
        
        # Nursing staff
        if label_upper in ('RN', 'RN-BSN', 'RN-MSN', 'LPN', 'CNA', 'NURSE'):
            return 'Nursing'
        
        # Physicians
        if label_upper in ('MD', 'DO', 'RES', 'RESIDENT', 'FELLOW', 'PA', 'NP'):
            return 'Physician'
        
        # Respiratory
        if label_upper in ('RT', 'RRT', 'RESPIRATORY'):
            return 'Respiratory'
        
        # Pharmacy
        if label_upper in ('PHARM', 'PHARMD', 'RPH'):
            return 'Pharmacy'
        
        # Read-only / System accounts
        if label_upper in ('RO', 'READ ONLY', 'SYSTEM'):
            return 'System'
            
        return 'Other'
    
    def transform_record(self, bronze: BronzeCaregivers) -> Dict[str, Any]:
        """
        Transform bronze caregiver to silver format.
        
        Transformations:
        - Validate caregiver ID
        - Standardize label (uppercase, trimmed)
        - Categorize role
        """
        # Skip records with invalid/missing cgid
        if not bronze.cgid:
            return None
        
        # Standardize label
        label = bronze.label.strip() if bronze.label else None
        
        # Standardize description
        description = bronze.description.strip() if bronze.description else None
        
        # Categorize role
        role_category = self._categorize_role(label)
        
        return {
            "cgid": bronze.cgid,
            "label": label,
            "description": description,
            "role_category": role_category,
        }
