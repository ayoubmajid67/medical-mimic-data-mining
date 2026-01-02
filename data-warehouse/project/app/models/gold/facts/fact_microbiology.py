"""Gold layer fact: Microbiology."""
from typing import Optional
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class FactMicrobiology(GoldBase):
    """Microbiology fact table."""
    
    __tablename__ = "fact_microbiology"
    __table_args__ = {"schema": "gold"}
    
    micro_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True, index=True)
    admission_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.fact_admission.admission_key"), nullable=True, index=True)
    
    row_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    chartdate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    charttime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    spec_type_desc: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    org_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, index=True)
    ab_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    interpretation: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    
    is_positive: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_resistant: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    def __repr__(self) -> str:
        return f"<FactMicrobiology(row_id={self.row_id})>"
