"""Gold layer fact: Procedure."""
from typing import Optional
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class FactProcedure(GoldBase):
    """Procedure fact table."""
    
    __tablename__ = "fact_procedure"
    __table_args__ = {"schema": "gold"}
    
    procedure_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True, index=True)
    admission_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.fact_admission.admission_key"), nullable=True, index=True)
    item_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_item.item_key"), nullable=True, index=True)
    
    row_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    starttime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    endtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    valueuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    is_completed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_canceled: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    duration_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    def __repr__(self) -> str:
        return f"<FactProcedure(row_id={self.row_id})>"
