"""Bronze models for INPUTEVENTS_CV and INPUTEVENTS_MV tables."""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BronzeBase


class BronzeInputEventsCareVue(BronzeBase):
    """
    Input events from CareVue system (2001-2008).
    
    Tracks fluids and medications administered via IV.
    """

    __tablename__ = "inputevents_cv"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    charttime: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="Chart timestamp")
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Item ID (FK to d_items)")
    
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Amount administered")
    amountuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Amount unit of measure")
    rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Rate of administration")
    rateuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Rate unit of measure")
    
    storetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Time recorded")
    cgid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Caregiver ID")
    orderid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Order ID")
    linkorderid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Linked order ID")
    
    stopped: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Stopped status")
    newbottle: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, comment="New bottle flag")
    
    originalamount: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Original amount ordered")
    originalamountuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Original amount UOM")
    originalroute: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Administration route")
    originalrate: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Original rate")
    originalrateuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Original rate UOM")
    originalsite: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Administration site")

    def __repr__(self) -> str:
        return f"<BronzeInputEventsCareVue(row_id={self.row_id}, itemid={self.itemid}, amount={self.amount})>"


class BronzeInputEventsMetaVision(BronzeBase):
    """
    Input events from MetaVision system (2008-2012).
    
    Tracks fluids and medications administered via IV.
    More detailed than CareVue.
    """

    __tablename__ = "inputevents_mv"
    __table_args__ = {"schema": "bronze"}

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Internal row identifier")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Patient ID")
    hadm_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="Hospital admission ID")
    icustay_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="ICU stay ID")
    
    starttime: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="Start timestamp")
    endtime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="End timestamp")
    itemid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Item ID (FK to d_items)")
    
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Amount administered")
    amountuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Amount unit of measure")
    rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Rate of administration")
    rateuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Rate unit of measure")
    
    storetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Time recorded")
    cgid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Caregiver ID")
    orderid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Order ID")
    linkorderid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="Linked order ID")
    
    ordercategoryname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Order category")
    secondaryordercategoryname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Secondary category")
    ordercomponenttypedescription: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Component type")
    ordercategorydescription: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Category description")
    
    patientweight: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Patient weight (kg)")
    totalamount: Mapped[Optional[float]] = mapped_column(Float, nullable =True, comment="Total amount")
    totalamountuom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Total amount UOM")
    
    isopenbag: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, comment="Is open bag")
    continueinnextdept: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, comment="Continue in next dept")
    cancelreason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Cancellation reason")
    statusdescription: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Status description")
    
    comments_editedby: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Edited by")
    comments_canceledby: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Canceled by")
    comments_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Comment date")
    
    originalamount: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Original amount")
    originalrate: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Original rate")

    def __repr__(self) -> str:
        return f"<BronzeInputEventsMetaVision(row_id={self.row_id}, itemid={self.itemid}, amount={self.amount})>"
