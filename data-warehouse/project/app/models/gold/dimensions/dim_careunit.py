"""Gold layer dimension: Care Unit."""
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class DimCareunit(GoldBase):
    """
    Care Unit dimension table.
    
    Contains ICU and other care unit definitions.
    """
    
    __tablename__ = "dim_careunit"
    __table_args__ = {"schema": "gold"}
    
    # Surrogate key
    careunit_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Natural key
    careunit: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    
    # Attributes
    unit_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="ICU, Ward, etc.")
    is_icu: Mapped[bool] = mapped_column(default=False, comment="Is this an ICU unit")

    def __repr__(self) -> str:
        return f"<DimCareunit(careunit_key={self.careunit_key}, careunit={self.careunit})>"
