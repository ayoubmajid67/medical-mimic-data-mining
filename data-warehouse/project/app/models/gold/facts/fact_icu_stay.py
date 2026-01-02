"""Gold layer fact: ICU Stay."""
from typing import Optional
from datetime import datetime, date

from sqlalchemy import Integer, String, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class FactIcuStay(GoldBase):
    """
    ICU Stay fact table.
    
    Contains metrics for each ICU stay.
    """
    
    __tablename__ = "fact_icu_stay"
    __table_args__ = {"schema": "gold"}
    
    # Surrogate key
    icu_stay_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Dimension foreign keys
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True, index=True)
    admission_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.fact_admission.admission_key"), nullable=True, index=True)
    in_date_key: Mapped[Optional[date]] = mapped_column(Date, ForeignKey("gold.dim_time.time_key"), nullable=True)
    
    # Natural keys
    icustay_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    # Care unit
    first_careunit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    last_careunit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Timestamps
    intime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    outtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Metrics
    los_icu_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    los_icu_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    def __repr__(self) -> str:
        return f"<FactIcuStay(icustay_id={self.icustay_id})>"
