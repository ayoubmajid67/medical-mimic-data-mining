"""Silver layer model for cleaned input events data."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverInputEvent(SilverBase):
    """
    Cleaned and unified input events from CareVue and MetaVision.
    
    Transformations from Bronze:
    - Unified both CV and MV systems into single table
    - Standardized units of measurement
    - Calculated infusion rates
    - Added source system flag
    """
    
    __tablename__ = "inputevents"
    __table_args__ = {"schema": "silver"}
    
    # Primary key
    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Row ID")
    
    # Foreign keys
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    # Source system
    source_system: Mapped[str] = mapped_column(String(20), nullable=False, comment="Source: CareVue or MetaVision")
    
    # Item information
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Item ID")
    
    # Timestamps
    charttime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True, comment="Chart time")
    starttime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Start time")
    endtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="End time")
    
    # Values (standardized)
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Amount given")
    amountuom: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, comment="Amount unit")
    rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Infusion rate")
    rateuom: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, comment="Rate unit")
    
    # Caregiver (FK to caregivers)
    cgid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Caregiver ID (FK to caregivers)")
    
    # Calculated fields
    duration_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Duration in hours")
    is_bolus: Mapped[bool] = mapped_column(default=False, comment="Is this a bolus dose")

    def __repr__(self) -> str:
        return f"<SilverInputEvent(row_id={self.row_id}, itemid={self.itemid})>"
