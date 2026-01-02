"""Bronze model for LABEVENTS table."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeLabEvents(BronzeBase):
    """
    Laboratory test results.
    
    Contains all lab measurements (blood tests, urine tests, etc.).
    High volume table.
    """

    __tablename__ = "labevents"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Hospital admission ID")
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Lab item ID (FK to d_labitems)")
    
    charttime: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="Lab measurement timestamp")
    value: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Result value (text)")
    valuenum: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Result value (numeric)")
    valueuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Unit of measurement")
    flag: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Abnormal flag")

    def __repr__(self) -> str:
        return f"<BronzeLabEvents(row_id={self.row_id}, itemid={self.itemid}, valuenum={self.valuenum})>"
