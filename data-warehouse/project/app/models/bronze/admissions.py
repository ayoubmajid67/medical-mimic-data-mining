"""Bronze model for ADMISSIONS table."""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeAdmissions(BronzeBase):
    """
    Hospital admission records.
    
    Tracks each visit to the hospital including admission type,
    location, diagnosis, and outcome.
    """

    __tablename__ = "admissions"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID (FK to patients)")
    hadm_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Unique hospital admission ID")
    
    admittime: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="Admission timestamp")
    dischtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Discharge timestamp")
    deathtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Death timestamp if died during admission")
    
    admission_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Type of admission (EMERGENCY, URGENT, ELECTIVE, NEWBORN)")
    admission_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Location prior to admission")
    discharge_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Discharge destination")
    
    insurance: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Insurance type")
    language: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Patient language")
    religion: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Patient religion")
    marital_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Marital status")
    ethnicity: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Patient ethnicity")
    
    edregtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="ED registration time")
    edouttime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="ED discharge time")
    
    diagnosis: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Preliminary diagnosis")
    hospital_expire_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="1 if died in hospital")
    has_chartevents_data: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="1 if chart data exists")

    def __repr__(self) -> str:
        return f"<BronzeAdmissions(hadm_id={self.hadm_id}, subject_id={self.subject_id}, admission_type={self.admission_type})>"
