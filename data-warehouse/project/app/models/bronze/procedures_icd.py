"""Bronze model for PROCEDURES_ICD table."""
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeProceduresICD(BronzeBase):
    """
    ICD-9 procedure codes assigned to hospital admissions.
    
    Records all procedures performed during a hospital stay using ICD-9
    procedure codes for billing and administrative purposes.
    """

    __tablename__ = "procedures_icd"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Hospital admission ID")
    
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False, comment="Sequence number for ordering")
    icd9_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, index=True, comment="ICD-9 procedure code")

    def __repr__(self) -> str:
        return f"<BronzeProceduresICD(row_id={self.row_id}, hadm_id={self.hadm_id}, icd9_code={self.icd9_code})>"
