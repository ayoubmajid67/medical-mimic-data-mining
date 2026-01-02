"""Gold layer aggregate: Lab Summary."""
from typing import Optional
from datetime import datetime

from sqlalchemy import Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class AggLabSummary(GoldBase):
    """
    Lab summary per patient/lab item.
    
    Pre-computed lab trends for analytics.
    """
    
    __tablename__ = "agg_lab_summary"
    __table_args__ = {"schema": "gold"}
    
    # Composite primary key
    summary_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Keys
    patient_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_patient.patient_key"), nullable=True, index=True)
    labitem_key: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gold.dim_labitem.labitem_key"), nullable=True, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    # Counts
    test_count: Mapped[int] = mapped_column(Integer, default=0)
    abnormal_count: Mapped[int] = mapped_column(Integer, default=0)
    abnormal_rate: Mapped[Float] = mapped_column(Float, nullable=True)
    
    # Statistics
    min_value: Mapped[Float] = mapped_column(Float, nullable=True)
    max_value: Mapped[Float] = mapped_column(Float, nullable=True)
    avg_value: Mapped[Float] = mapped_column(Float, nullable=True)
    std_value: Mapped[Float] = mapped_column(Float, nullable=True)
    
    # Dates
    first_test: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_test: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<AggLabSummary(subject_id={self.subject_id}, itemid={self.itemid})>"
