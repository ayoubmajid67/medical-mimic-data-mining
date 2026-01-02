"""Gold layer fact: Input Event."""
from typing import Optional
from datetime import datetime, date

from sqlalchemy import Integer, String, Boolean, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class FactInputEvent(GoldBase):
    """Input Event fact table (unified CV + MV)."""
    
    __tablename__ = "fact_input_event"
    __table_args__ = {"schema": "gold"}
    
    input_event_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True, index=True)
    admission_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.fact_admission.admission_key"), nullable=True, index=True)
    item_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_item.item_key"), nullable=True, index=True)
    caregiver_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_caregiver.caregiver_key"), nullable=True, index=True)
    
    row_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    cgid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Caregiver ID")
    
    source_system: Mapped[str] = mapped_column(String(20), nullable=False)
    charttime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    amountuom: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rateuom: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    duration_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_bolus: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    def __repr__(self) -> str:
        return f"<FactInputEvent(row_id={self.row_id})>"
