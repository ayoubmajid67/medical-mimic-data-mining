"""Gold layer aggregate: Medication Usage."""
from typing import Optional

from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class AggMedicationUsage(GoldBase):
    """
    Medication usage patterns aggregate.
    
    One row per drug with usage statistics.
    """
    
    __tablename__ = "agg_medication_usage"
    __table_args__ = {"schema": "gold"}
    
    # Primary key
    drug: Mapped[str] = mapped_column(String(200), primary_key=True)
    
    # Attributes
    drug_name_generic: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # Counts
    prescription_count: Mapped[int] = mapped_column(Integer, default=0)
    patient_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Duration
    avg_duration_days: Mapped[Float] = mapped_column(Float, nullable=True)
    total_duration_days: Mapped[Float] = mapped_column(Float, nullable=True)
    
    # Common patterns
    most_common_route: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    most_common_dose: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<AggMedicationUsage(drug={self.drug})>"
