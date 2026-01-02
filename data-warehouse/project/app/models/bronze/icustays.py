"""Bronze model for ICUSTAYS table."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeICUStays(BronzeBase):
    """
    ICU stay records.
    
    Tracks time spent in Intensive Care Units during hospital admissions.
    """

    __tablename__ = "icustays"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Unique ICU stay identifier")
    
    dbsource: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="Database source (carevue/metavision)")
    first_careunit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="First ICU care unit")
    last_careunit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Last ICU care unit")
    first_wardid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="First ward ID")
    last_wardid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Last ward ID")
    
    intime: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="ICU admission timestamp")
    outtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="ICU discharge timestamp")
    los: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Length of stay in days")

    def __repr__(self) -> str:
        return f"<BronzeICUStays(icustay_id={self.icustay_id}, subject_id={self.subject_id}, los={self.los})>"
