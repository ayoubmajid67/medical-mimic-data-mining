"""Gold layer fact: Prescription."""
from typing import Optional
from datetime import datetime, date

from sqlalchemy import Integer, String, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class FactPrescription(GoldBase):
    """
    Prescription fact table.
    """
    
    __tablename__ = "fact_prescription"
    __table_args__ = {"schema": "gold"}
    
    prescription_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True, index=True)
    admission_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.fact_admission.admission_key"), nullable=True, index=True)
    start_date_key: Mapped[Optional[date]] = mapped_column(Date, ForeignKey("gold.dim_time.time_key"), nullable=True)
    
    row_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    drug: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, index=True)
    drug_name_generic: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    drug_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    startdate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    enddate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    dose_val: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dose_unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    route: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    duration_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    def __repr__(self) -> str:
        return f"<FactPrescription(row_id={self.row_id})>"
