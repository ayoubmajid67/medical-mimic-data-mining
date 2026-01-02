"""Gold layer aggregate: Infection Statistics."""
from typing import Optional

from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class AggInfectionStats(GoldBase):
    """
    Infection/microbiology statistics aggregate.
    
    One row per organism with resistance patterns.
    """
    
    __tablename__ = "agg_infection_stats"
    __table_args__ = {"schema": "gold"}
    
    # Primary key
    organism_name: Mapped[str] = mapped_column(String(200), primary_key=True)
    
    # Culture counts
    total_cultures: Mapped[int] = mapped_column(Integer, default=0)
    positive_cultures: Mapped[int] = mapped_column(Integer, default=0)
    positive_rate: Mapped[Float] = mapped_column(Float, nullable=True)
    
    # Resistance
    resistance_tests: Mapped[int] = mapped_column(Integer, default=0)
    resistant_count: Mapped[int] = mapped_column(Integer, default=0)
    resistance_rate: Mapped[Float] = mapped_column(Float, nullable=True)
    
    # Common specimen
    most_common_spec: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<AggInfectionStats(organism_name={self.organism_name})>"
