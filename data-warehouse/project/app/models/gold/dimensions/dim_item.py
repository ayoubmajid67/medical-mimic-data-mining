"""Gold layer dimension: Item (from d_items)."""
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class DimItem(GoldBase):
    """
    Item dimension table.
    
    Contains item definitions from MIMIC d_items table.
    Used for chartevents, inputevents, outputevents, etc.
    """
    
    __tablename__ = "dim_item"
    __table_args__ = {"schema": "gold"}
    
    # Surrogate key
    item_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Natural key
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    
    # Attributes
    label: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    abbreviation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    dbsource: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="carevue/metavision")
    linksto: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    unitname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    param_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    conceptid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<DimItem(item_key={self.item_key}, itemid={self.itemid})>"
