"""Gold layer dimension: Caregiver."""
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class DimCaregiver(GoldBase):
    """
    Caregiver dimension table.
    
    Contains caregiver/staff definitions.
    """
    
    __tablename__ = "dim_caregiver"
    __table_args__ = {"schema": "gold"}
    
    # Surrogate key
    caregiver_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Natural key
    cgid: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    
    # Attributes
    label: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<DimCaregiver(cgid={self.cgid})>"
