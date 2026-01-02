"""Bronze model for NOTEEVENTS table."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeNoteEvents(BronzeBase):
    """
    Clinical notes and discharge summaries.
    
    Contains free-text notes written by healthcare providers.
    This table was empty in the sample dataset but structure is defined
    based on standard MIMIC-III schema.
    """

    __tablename__ = "noteevents"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Hospital admission ID")
    
    chartdate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Chart date")
    charttime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True, comment="Chart timestamp")
    storetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Time note was recorded")
    
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Note category")
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Note description")
    cgid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Caregiver ID")
    
    iserror: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, comment="Error flag")
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Full text of note")

    def __repr__(self) -> str:
        return f"<BronzeNoteEvents(row_id={self.row_id}, category={self.category})>"
