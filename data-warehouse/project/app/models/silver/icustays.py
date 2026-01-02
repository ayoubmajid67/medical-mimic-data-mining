"""Silver layer model for cleaned ICU stay data."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverICUStay(SilverBase):
    """
    Cleaned and enriched ICU stay data.
    
    Transformations from Bronze:
    - Validated in/out times
    - Calculated ICU length of stay
    - Standardized care unit names
    - Added ICU sequence number
    """
    
    __tablename__ = "icustays"
    __table_args__ = {"schema": "silver"}
    
    # Primary key
    icustay_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="ICU stay ID")
    
    # Foreign keys
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Hospital admission ID")
    
    # ICU details
    first_careunit: Mapped[str] = mapped_column(String(50), nullable=False, comment="First care unit")
    last_careunit: Mapped[str] = mapped_column(String(50), nullable=False, comment="Last care unit")
    first_wardid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="First ward ID")
    last_wardid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Last ward ID")
    
    # Timestamps (validated)
    intime: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="ICU admission time")
    outtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="ICU discharge time")
    
    # Calculated fields
    los_icu_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="ICU length of stay in days")
    los_icu_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="ICU length of stay in hours")

    def __repr__(self) -> str:
        return f"<SilverICUStay(icustay_id={self.icustay_id}, hadm_id={self.hadm_id})>"
