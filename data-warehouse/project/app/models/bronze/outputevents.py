"""Bronze model for OUTPUTEVENTS table."""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeOutputEvents(BronzeBase):
    """
    Output events (urine, drainage, etc.).
    
    Tracks fluid output from patients.
    """

    __tablename__ = "outputevents"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    charttime: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="Chart timestamp")
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Item ID (FK to d_items)")
    
    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Output value")
    valueuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Value unit of measure")
    
    storetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Time recorded")
    cgid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Caregiver ID")
    
    stopped: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Stopped status")
    newbottle: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, comment="New bottle flag")
    iserror: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, comment="Error flag")

    def __repr__(self) -> str:
        return f"<BronzeOutputEvents(row_id={self.row_id}, itemid={self.itemid}, value={self.value})>"
