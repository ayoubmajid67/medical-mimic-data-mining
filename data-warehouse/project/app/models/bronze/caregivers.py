"""Bronze model for CAREGIVERS table."""
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeCaregivers(BronzeBase):
    """
    Caregiver role definitions.
    
    Defines healthcare providers (nurses, doctors, etc.) who provided care.
    """

    __tablename__ = "caregivers"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="Internal row identifier")
    cgid: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Unique caregiver identifier")
    
    label: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Role code (RN, MD, etc)")
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Full role description")

    def __repr__(self) -> str:
        return f"<BronzeCaregivers(cgid={self.cgid}, label={self.label})>"

