"""Silver layer model for cleaned procedure events data."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverProcedureEvent(SilverBase):
    """
    Cleaned and enriched procedure events data.
    
    Transformations from Bronze:
    - Calculated procedure duration
    - Standardized status codes
    - Added completion flag
    """
    
    __tablename__ = "procedureevents"
    __table_args__ = {"schema": "silver"}
    
    # Primary key
    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Row ID")
    
    # Foreign keys
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    # Procedure details
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Item ID")
    starttime: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="Start time")
    endtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="End time")
    
    # Values
    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Procedure value")
    valueuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Unit of measurement")
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Body location")
    
    # Status
    status_description: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Status")
    is_completed: Mapped[bool] = mapped_column(default=True, comment="Was procedure completed")
    is_canceled: Mapped[bool] = mapped_column(default=False, comment="Was procedure canceled")
    
    # Calculated fields
    duration_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Duration in hours")

    def __repr__(self) -> str:
        return f"<SilverProcedureEvent(row_id={self.row_id}, itemid={self.itemid})>"
