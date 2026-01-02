"""Silver layer model for cleaned output events data."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverOutputEvent(SilverBase):
    """
    Cleaned and enriched output events data.
    
    Transformations from Bronze:
    - Standardized units of measurement
    - Parsed numeric values
    - Categorized output types
    """
    
    __tablename__ = "outputevents"
    __table_args__ = {"schema": "silver"}
    
    # Primary key
    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Row ID")
    
    # Foreign keys
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    # Output details
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Item ID")
    charttime: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="Chart time")
    
    # Values (cleaned)
    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Output value")
    valueuom: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, comment="Unit of measurement")
    
    # Caregiver
    cgid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Caregiver ID")

    def __repr__(self) -> str:
        return f"<SilverOutputEvent(row_id={self.row_id}, itemid={self.itemid})>"
