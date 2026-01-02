"""Gold layer aggregate: ICU Performance."""
from typing import Optional

from sqlalchemy import String, Integer, Float, text
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class AggIcuPerformance(GoldBase):
    """
    ICU unit performance KPIs.
    
    One row per care unit with aggregate metrics.
    """
    
    __tablename__ = "agg_icu_performance"
    __table_args__ = {"schema": "gold"}
    
    # Primary key
    careunit: Mapped[str] = mapped_column(String(50), primary_key=True)
    
    # Volume
    total_stays: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    total_patients: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    
    # Length of Stay
    avg_los_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    median_los_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_los_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Outcomes
    mortality_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    mortality_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Readmissions
    readmit_48h_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    readmit_48h_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Activity
    avg_labs_per_stay: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    def __repr__(self) -> str:
        return f"<AggIcuPerformance(careunit={self.careunit})>"

