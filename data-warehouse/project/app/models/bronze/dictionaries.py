"""Bronze models for dictionary tables (D_ITEMS, D_LABITEMS)."""
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeDItems(BronzeBase):
    """
    Dictionary for item definitions.
    
    Defines labels and metadata for items referenced in event tables
    (chartevents, inputevents, outputevents, procedureevents).
    """

    __tablename__ = "d_items"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="Internal row identifier")
    itemid: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Unique item identifier")
    
    label: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Item label/name")
    abbreviation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Item abbreviation")
    dbsource: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="Database source")
    linksto: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Table this item links to")
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Item category")
    unitname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Unit of measurement")
    param_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, comment="Parameter type")
    conceptid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Concept ID mapping")

    def __repr__(self) -> str:
        return f"<BronzeDItems(itemid={self.itemid}, label={self.label})>"


class BronzeDLabItems(BronzeBase):
    """
    Dictionary for laboratory test items.
    
    Defines labels and metadata for lab tests referenced in labevents.
    """

    __tablename__ = "d_labitems"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="Internal row identifier")
    itemid: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Unique lab item identifier")
    
    label: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Lab test name")
    fluid: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Fluid tested (Blood, Urine, etc)")
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Lab test category")
    loinc_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="LOINC code mapping")

    def __repr__(self) -> str:
        return f"<BronzeDLabItems(itemid={self.itemid}, label={self.label}, fluid={self.fluid})>"
