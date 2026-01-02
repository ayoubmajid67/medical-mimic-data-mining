"""Silver layer model for cleaned lab events data."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import SilverBase


class SilverLabEvent(SilverBase):
    """
    Cleaned and enriched lab event data.
    
    Transformations from Bronze:
    - Parsed numeric values from strings
    - Standardized units of measurement
    - Flagged abnormal results
    - Added reference range comparisons
    """
    
    __tablename__ = "labevents"
    __table_args__ = {"schema": "silver"}
    
    # Primary key (composite in bronze, simplified here)
    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Row ID")
    
    # Foreign keys
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Hospital admission ID")
    
    # Lab test details
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Lab item ID")
    charttime: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="Chart time")
    
    # Values (cleaned)
    value: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Original value string")
    valuenum: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Numeric value")
    valueuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Unit of measurement")
    
    # Flags
    flag: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="Abnormal flag")
    is_abnormal: Mapped[bool] = mapped_column(Boolean, default=False, comment="Is result abnormal")

    def __repr__(self) -> str:
        return f"<SilverLabEvent(row_id={self.row_id}, itemid={self.itemid})>"
