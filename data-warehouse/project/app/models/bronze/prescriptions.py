"""Bronze model for PRESCRIPTIONS table."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzePrescriptions(BronzeBase):
    """
    Medication prescriptions.
    
    Contains all medication orders for patients.
    """

    __tablename__ = "prescriptions"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    startdate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Prescription start date")
    enddate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Prescription end date")
    
    drug_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Drug type (MAIN/BASE)")
    drug: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Drug name")
    drug_name_poe: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Drug name (POE)")
    drug_name_generic: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Generic drug name")
    
    formulary_drug_cd: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Formulary drug code")
    gsn: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="GSN code")
    ndc: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="National Drug Code")
    prod_strength: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Product strength")
    
    dose_val_rx: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Dose value")
    dose_unit_rx: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Dose unit")
    form_val_disp: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Form value dispensed")
    form_unit_disp: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Form unit dispensed")
    route: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Administration route")

    def __repr__(self) -> str:
        return f"<BronzePrescriptions(row_id={self.row_id}, drug={self.drug}, route={self.route})>"
