"""Bronze model for PROCEDUREEVENTS_MV table."""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeProcedureEventsMetaVision(BronzeBase):
    """
    Procedure events from MetaVision system.
    
    Tracks medical procedures performed on patients (e.g., ventilation, dialysis).
    """

    __tablename__ = "procedureevents_mv"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    starttime: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="Procedure start time")
    endtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Procedure end time")
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Item ID (FK to d_items)")
    
    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Value (e.g., duration)")
    valueuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Value unit of measure")
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Body location")
    locationcategory: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Location category")
    
    storetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Time recorded")
    cgid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Caregiver ID")
    orderid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Order ID")
    linkorderid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Linked order ID")
    
    ordercategoryname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Order category")
    secondaryordercategoryname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Secondary category")
    ordercategorydescription: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Category description")
    
    isopenbag: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, comment="Is open bag")
    continueinnextdept: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, comment="Continue in next dept")
    cancelreason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Cancellation reason")
    statusdescription: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Status description")
    
    comments_editedby: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Edited by")
    comments_canceledby: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Canceled by")
    comments_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Comment date")

    def __repr__(self) -> str:
        return f"<BronzeProcedureEventsMetaVision(row_id={self.row_id}, itemid={self.itemid})>"
