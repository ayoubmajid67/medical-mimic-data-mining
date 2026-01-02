"""Silver layer model for cleaned caregiver data."""
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverCaregiver(SilverBase):
    """
    Cleaned and validated caregiver data.
    
    Transformations from Bronze:
    - Validated caregiver IDs
    - Standardized labels and descriptions
    - Removed invalid or duplicate records
    """
    
    __tablename__ = "caregivers"
    __table_args__ = {"schema": "silver"}
    
    # Primary key (natural key from source)
    cgid: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Unique caregiver identifier")
    
    # Attributes (cleaned/validated)
    label: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, 
        comment="Role code (RN, MD, RT, etc)"
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, 
        comment="Full role description"
    )
    
    # Derived/enriched fields
    role_category: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True,
        comment="Categorized role (Nursing, Physician, Respiratory, etc)"
    )

    def __repr__(self) -> str:
        return f"<SilverCaregiver(cgid={self.cgid}, label={self.label})>"
