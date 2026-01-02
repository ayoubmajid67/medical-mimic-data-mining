"""Silver layer model for cleaned transfer data."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverTransfer(SilverBase):
    """
    Cleaned and enriched transfer data.
    
    Transformations from Bronze:
    - Calculated transfer duration
    - Standardized care unit names
    - Added transfer sequence numbers
    - Identified transfer patterns
    """
    
    __tablename__ = "transfers"
    __table_args__ = {"schema": "silver"}
    
    # Primary key
    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Row ID")
    
    # Foreign keys
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    # Location information
    eventtype: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="Event type (admit/transfer/discharge)")
    prev_careunit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Previous care unit")
    curr_careunit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Current care unit")
    prev_wardid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Previous ward ID")
    curr_wardid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Current ward ID")
    
    # Timestamps
    intime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True, comment="Transfer in time")
    outtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Transfer out time")
    
    # Calculated fields
    duration_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Duration in hours")
    is_icu_transfer: Mapped[bool] = mapped_column(default=False, comment="Is this an ICU transfer")

    def __repr__(self) -> str:
        return f"<SilverTransfer(row_id={self.row_id}, curr_careunit={self.curr_careunit})>"
