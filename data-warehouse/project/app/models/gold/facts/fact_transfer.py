"""Gold layer fact: Transfer."""
from typing import Optional
from datetime import datetime, date

from sqlalchemy import Integer, String, Boolean, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class FactTransfer(GoldBase):
    """Transfer fact table."""
    
    __tablename__ = "fact_transfer"
    __table_args__ = {"schema": "gold"}
    
    transfer_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True, index=True)
    admission_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.fact_admission.admission_key"), nullable=True, index=True)
    
    row_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    eventtype: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    prev_careunit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    curr_careunit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    
    intime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    outtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    duration_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_icu_transfer: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<FactTransfer(row_id={self.row_id})>"
