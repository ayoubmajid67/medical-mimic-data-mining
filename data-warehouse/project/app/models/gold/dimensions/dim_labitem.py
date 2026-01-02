"""Gold layer dimension: Lab Item (from d_labitems)."""
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class DimLabitem(GoldBase):
    """
    Lab Item dimension table.
    
    Contains lab test definitions from MIMIC d_labitems table.
    """
    
    __tablename__ = "dim_labitem"
    __table_args__ = {"schema": "gold"}
    
    # Surrogate key
    labitem_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Natural key
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    
    # Attributes
    label: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, index=True)
    fluid: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    loinc_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<DimLabitem(labitem_key={self.labitem_key}, label={self.label})>"
