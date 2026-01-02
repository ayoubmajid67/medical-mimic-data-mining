"""Gold layer fact: Admission."""
from typing import Optional
from datetime import datetime, date

from sqlalchemy import Integer, String, Boolean, DateTime, Float, Date, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class FactAdmission(GoldBase):
    """
    Admission fact table.
    
    Central fact table with pre-calculated metrics per admission.
    """
    
    __tablename__ = "fact_admission"
    __table_args__ = {"schema": "gold"}
    
    # Surrogate key
    admission_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Dimension foreign keys
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True, index=True)
    admit_date_key: Mapped[Optional[date]] = mapped_column(Date, ForeignKey("gold.dim_time.time_key"), nullable=True)
    disch_date_key: Mapped[Optional[date]] = mapped_column(Date, ForeignKey("gold.dim_time.time_key"), nullable=True)
    
    # Natural keys
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    # Admission attributes
    admission_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    admission_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    discharge_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    insurance: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Timestamps
    admittime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    dischtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Metrics - Length of Stay
    los_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    los_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    icu_los_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Metrics - Counts (nullable to allow INSERT without explicit values)
    num_icu_stays: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    num_lab_tests: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    num_prescriptions: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    num_procedures: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    num_transfers: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    
    # Outcomes
    hospital_expire: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, server_default=text("false"))
    is_readmit_30day: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, server_default=text("false"))
    days_to_readmit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<FactAdmission(hadm_id={self.hadm_id})>"

