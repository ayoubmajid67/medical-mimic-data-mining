"""Bronze model for MICROBIOLOGYEVENTS table."""
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeMicrobiologyEvents(BronzeBase):
    """
    Microbiology culture and sensitivity results.
    
    Tracks bacterial cultures and antibiotic sensitivity testing.
    """

    __tablename__ = "microbiologyevents"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Hospital admission ID")
    
    chartdate: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="Chart date")
    charttime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True, comment="Chart timestamp")
    
    spec_itemid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Specimen item ID")
    spec_type_desc: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Specimen type description")
    
    org_itemid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Organism item ID")
    org_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Organism name")
    isolate_num: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Isolate number")
    
    ab_itemid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Antibiotic item ID")
    ab_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Antibiotic name")
    
    dilution_text: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Dilution text")
    dilution_comparison: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, comment="Comparison operator")
    dilution_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Dilution value")
    interpretation: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, comment="Interpretation (S/I/R)")

    def __repr__(self) -> str:
        return f"<BronzeMicrobiologyEvents(row_id={self.row_id}, org_name={self.org_name}, interpretation={self.interpretation})>"
