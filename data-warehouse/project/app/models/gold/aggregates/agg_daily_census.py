"""Gold layer aggregate: Daily Census."""
from typing import Optional
from datetime import date

from sqlalchemy import Date, Integer, Float, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class AggDailyCensus(GoldBase):
    """
    Daily hospital census aggregate.
    
    One row per day with key operational metrics.
    """
    
    __tablename__ = "agg_daily_census"
    __table_args__ = {"schema": "gold"}
    
    # Primary key
    date_key: Mapped[date] = mapped_column(Date, ForeignKey("gold.dim_time.time_key"), primary_key=True)
    
    # Patient counts
    active_patients: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"), comment="Patients in hospital at midnight")
    new_admissions: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    discharges: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    deaths: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    
    # ICU metrics
    icu_patients: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    new_icu_admits: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    icu_discharges: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, server_default=text("0"))
    
    # Averages
    avg_los_discharged: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    def __repr__(self) -> str:
        return f"<AggDailyCensus(date_key={self.date_key})>"

