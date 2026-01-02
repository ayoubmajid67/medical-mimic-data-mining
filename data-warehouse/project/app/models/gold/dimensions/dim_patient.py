"""Gold layer dimension: Patient."""
from typing import Optional
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class DimPatient(GoldBase):
    """
    Patient dimension table.
    
    Provides patient demographics with pre-calculated age groups
    and lifetime statistics for efficient analytics.
    """
    
    __tablename__ = "dim_patient"
    __table_args__ = {"schema": "gold"}
    
    # Surrogate key
    patient_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Natural key
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    
    # Demographics
    gender: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    age_group: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="0-17, 18-44, 45-64, 65-84, 85+")
    
    # Status
    is_deceased: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Pre-calculated lifetime stats
    total_admissions: Mapped[int] = mapped_column(Integer, default=0)
    total_icu_stays: Mapped[int] = mapped_column(Integer, default=0)
    
    # Date range
    first_admission: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_admission: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<DimPatient(patient_key={self.patient_key}, subject_id={self.subject_id})>"
