"""Bronze model for TRANSFERS table."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeTransfers(BronzeBase):
    """
    Patient transfers and movements.
    
    Tracks physical movement of patients between hospital locations.
    """

    __tablename__ = "transfers"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    dbsource: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="Database source")
    eventtype: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Event type (admit/transfer/discharge)")
    
    prev_careunit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Previous care unit")
    curr_careunit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Current care unit")
    prev_wardid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Previous ward ID")
    curr_wardid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Current ward ID")
    
    intime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Transfer in timestamp")
    outtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Transfer out timestamp")
    los: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Length of stay in hours")

    def __repr__(self) -> str:
        return f"<BronzeTransfers(hadm_id={self.hadm_id}, eventtype={self.eventtype})>"
