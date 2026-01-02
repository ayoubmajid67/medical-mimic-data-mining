"""Gold layer fact: Output Event."""
from typing import Optional
from datetime import datetime

from sqlalchemy import Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class FactOutputEvent(GoldBase):
    """Output Event fact table."""
    
    __tablename__ = "fact_output_event"
    __table_args__ = {"schema": "gold"}
    
    output_event_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True, index=True)
    admission_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.fact_admission.admission_key"), nullable=True, index=True)
    item_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_item.item_key"), nullable=True, index=True)
    
    row_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    charttime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    def __repr__(self) -> str:
        return f"<FactOutputEvent(row_id={self.row_id})>"
