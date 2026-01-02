"""Silver layer model for cleaned microbiology events data."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverMicrobiologyEvent(SilverBase):
    """
    Cleaned and enriched microbiology events data.
    
    Transformations from Bronze:
    - Standardized organism names
    - Parsed susceptibility results
    - Added resistance flags
    """
    
    __tablename__ = "microbiologyevents"
    __table_args__ = {"schema": "silver"}
    
    # Primary key
    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Row ID")
    
    # Foreign keys
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Hospital admission ID")
    
    # Timestamps
    chartdate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Chart date")
    charttime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True, comment="Chart time")
    
    # Specimen
    spec_itemid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Specimen item ID")
    spec_type_desc: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Specimen type")
    
    # Organism
    org_itemid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Organism item ID")
    org_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, index=True, comment="Organism name")
    
    # Antibiotic susceptibility
    ab_itemid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Antibiotic item ID")
    ab_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Antibiotic name")
    dilution_text: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Dilution text")
    interpretation: Mapped[Optional[str]] = mapped_column(String(5), nullable=True, comment="S/I/R interpretation")
    
    # Derived flags
    is_positive: Mapped[bool] = mapped_column(default=False, comment="Positive culture result")
    is_resistant: Mapped[bool] = mapped_column(default=False, comment="Antibiotic resistant")

    def __repr__(self) -> str:
        return f"<SilverMicrobiologyEvent(row_id={self.row_id}, org_name={self.org_name})>"
