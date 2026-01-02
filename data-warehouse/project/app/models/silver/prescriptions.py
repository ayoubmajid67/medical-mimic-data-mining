"""Silver layer model for cleaned prescription data."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverPrescription(SilverBase):
    """
    Cleaned and enriched prescription data.
    
    Transformations from Bronze:
    - Standardized drug names
    - Parsed dosage values
    - Calculated duration days
    - Normalized route of administration
    """
    
    __tablename__ = "prescriptions"
    __table_args__ = {"schema": "silver"}
    
    # Primary key
    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Row ID")
    
    # Foreign keys
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    # Timestamps
    startdate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Start date")
    enddate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="End date")
    
    # Drug information (cleaned)
    drug_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Drug type")
    drug: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, index=True, comment="Drug name")
    drug_name_generic: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Generic name")
    formulary_drug_cd: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Formulary code")
    
    # Dosage (parsed)
    dose_val_rx: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Dose value")
    dose_unit_rx: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Dose unit")
    form_val_disp: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Form value dispensed")
    form_unit_disp: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Form unit dispensed")
    
    # Administration
    route: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Route of administration")
    
    # Calculated fields
    duration_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Duration in days")

    def __repr__(self) -> str:
        return f"<SilverPrescription(row_id={self.row_id}, drug={self.drug})>"
