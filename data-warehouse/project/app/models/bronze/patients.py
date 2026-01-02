"""Bronze model for PATIENTS table."""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzePatients(BronzeBase):
    """
    Patient demographics and survival information.
    
    This is the root entity - all other tables link back to patients
    via subject_id.
    """

    __tablename__ = "patients"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Unique patient identifier")
    gender: Mapped[str] = mapped_column(String(1), nullable=False, comment="Patient gender (M/F)")
    dob: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="Date of birth (shifted for anonymity)")
    dod: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Date of death")
    dod_hosp: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, comment="Date of death recorded in hospital"
    )
    dod_ssn: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, comment="Date of death from social security records"
    )
    expire_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="1 if patient died, 0 if alive")

    def __repr__(self) -> str:
        return f"<BronzePatients(subject_id={self.subject_id}, gender={self.gender}, expire_flag={self.expire_flag})>"
