"""Gold layer dimension: Procedure ICD."""
from typing import Optional

from sqlalchemy import Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class DimProcedureIcd(GoldBase):
    """
    Procedure ICD dimension table.
    
    Contains ICD-9 procedure code definitions.
    """
    
    __tablename__ = "dim_procedure_icd"
    __table_args__ = {"schema": "gold"}
    
    # Surrogate key
    procedure_icd_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Natural key
    icd9_code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True, index=True)
    
    # Attributes
    short_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    long_title: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    seq_num: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True, comment="Sequence number")

    def __repr__(self) -> str:
        return f"<DimProcedureIcd(icd9_code={self.icd9_code})>"
