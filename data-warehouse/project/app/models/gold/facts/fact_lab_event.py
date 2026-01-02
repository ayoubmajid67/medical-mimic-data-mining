"""Gold layer fact: Lab Event."""
from typing import Optional
from datetime import datetime, date

from sqlalchemy import Integer, String, Boolean, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class FactLabEvent(GoldBase):
    """
    Lab Event fact table.
    
    Contains individual lab test results.
    """
    
    __tablename__ = "fact_lab_event"
    __table_args__ = {"schema": "gold"}
    
    # Surrogate key
    lab_event_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Dimension foreign keys
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True, index=True)
    admission_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.fact_admission.admission_key"), nullable=True, index=True)
    labitem_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_labitem.labitem_key"), nullable=True, index=True)
    chart_date_key: Mapped[Optional[date]] = mapped_column(Date, ForeignKey("gold.dim_time.time_key"), nullable=True)
    
    # Natural keys
    row_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    # Timestamps
    charttime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Values
    value: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    valuenum: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    valueuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Flags
    is_abnormal: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<FactLabEvent(row_id={self.row_id})>"
