"""Silver layer model for cleaned patient data."""
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverPatient(SilverBase):
    """
    Cleaned and validated patient data.
    
    Transformations from Bronze:
    - Validated date formats
    - Standardized gender codes (M/F)
    - Calculated age at various events
    - Removed invalid records
    """
    
    __tablename__ = "patients"
    __table_args__ = {"schema": "silver"}
    
    # Primary key
    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Patient ID")
    
    # Demographics
    gender: Mapped[str] = mapped_column(String(1), nullable=False, comment="Gender (M/F)")
    
    # Dates (validated)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="Date of birth")
    date_of_death: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="Date of death")
    
    # Calculated fields
    is_deceased: Mapped[bool] = mapped_column(default=False, comment="Whether patient is deceased")
    
    # Data quality
    dob_shift_years: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True, 
        comment="Years DOB was shifted (for patients > 89)"
    )

    def __repr__(self) -> str:
        return f"<SilverPatient(subject_id={self.subject_id}, gender={self.gender})>"
