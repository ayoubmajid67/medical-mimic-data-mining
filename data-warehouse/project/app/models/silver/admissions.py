"""Silver layer model for cleaned admission data."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverAdmission(SilverBase):
    """
    Cleaned and enriched admission data.
    
    Transformations from Bronze:
    - Validated admission/discharge times
    - Standardized admission types
    - Calculated length of stay
    - Linked mortality indicators
    """
    
    __tablename__ = "admissions"
    __table_args__ = {"schema": "silver"}
    
    # Primary key
    hadm_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Hospital admission ID")
    
    # Foreign keys
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    
    # Admission details
    admission_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="Admission type (EMERGENCY, ELECTIVE, etc.)")
    admission_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Where patient was admitted from")
    discharge_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Where patient was discharged to")
    
    # Timestamps (validated)
    admittime: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="Admission time")
    dischtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Discharge time")
    edregtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="ED registration time")
    edouttime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="ED out time")
    
    # Calculated fields
    los_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Length of stay in days")
    los_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Length of stay in hours")
    
    # Diagnosis
    diagnosis: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="Primary diagnosis")
    
    # Mortality
    hospital_expire_flag: Mapped[bool] = mapped_column(Boolean, default=False, comment="Died during hospital stay")
    
    # Insurance/Demographics
    insurance: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Insurance type")
    language: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="Language")
    religion: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Religion")
    marital_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Marital status")
    ethnicity: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Ethnicity")

    def __repr__(self) -> str:
        return f"<SilverAdmission(hadm_id={self.hadm_id}, subject_id={self.subject_id})>"
