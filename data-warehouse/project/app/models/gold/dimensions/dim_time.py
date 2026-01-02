"""Gold layer dimension: Time."""
from sqlalchemy import Date, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class DimTime(GoldBase):
    """
    Time/Date dimension table.
    
    Pre-generated date dimension for efficient date-based analytics.
    Covers date range from data (2100-2200 for MIMIC shifted dates).
    """
    
    __tablename__ = "dim_time"
    __table_args__ = {"schema": "gold"}
    
    # Primary key is the date itself
    time_key: Mapped[Date] = mapped_column(Date, primary_key=True)
    
    # Year components
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    quarter: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month_name: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Week components
    week_of_year: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Day components
    day_of_month: Mapped[int] = mapped_column(Integer, nullable=False)
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    day_name: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Flags
    is_weekend: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"<DimTime(time_key={self.time_key})>"
