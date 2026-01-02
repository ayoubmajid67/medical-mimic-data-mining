"""Gold layer aggregate: Patient Summary."""
from typing import Optional
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Float, DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class AggPatientSummary(GoldBase):
    """
    Patient lifetime summary aggregate.
    
    Pre-computed statistics for each patient across all admissions.
    """
    
    __tablename__ = "agg_patient_summary"
    __table_args__ = {"schema": "gold"}
    
    # Primary key = natural key
    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # FK to dimension
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True)
    
    # Demographics
    gender: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    age_group: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    is_deceased: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, server_default=text("false"))
    
    # Counts - all nullable with server defaults
    total_admissions: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    total_icu_stays: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    total_lab_tests: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    total_prescriptions: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    total_procedures: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    
    # Length of Stay
    total_los_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True, server_default=text("0"))
    avg_los_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_icu_los_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True, server_default=text("0"))
    
    # Dates
    first_admission: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_admission: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Readmissions
    readmit_30day_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))

    def __repr__(self) -> str:
        return f"<AggPatientSummary(subject_id={self.subject_id})>"

