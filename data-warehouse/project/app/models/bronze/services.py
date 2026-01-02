"""Bronze model for SERVICES table."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeServices(BronzeBase):
    """
    Medical service assignments.
    
    Tracks which medical service (team) was responsible for patient care
    at different points during a hospital admission.
    
    Examples of services: MED (Medicine), SURG (Surgery), CMED (Cardiac Medicine),
    TRAUM (Trauma), NMED (Neurology), etc.
    """

    __tablename__ = "services"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Hospital admission ID")
    
    transfertime: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="Service transfer timestamp")
    prev_service: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Previous service")
    curr_service: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Current service")

    def __repr__(self) -> str:
        return f"<BronzeServices(row_id={self.row_id}, hadm_id={self.hadm_id}, curr_service={self.curr_service})>"
