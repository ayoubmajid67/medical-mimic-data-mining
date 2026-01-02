"""Silver layer base model."""
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class SilverBase(DeclarativeBase):
    """
    Base class for all Silver layer models.
    
    Silver layer contains cleaned, validated, and standardized data.
    All records include audit timestamps for tracking data lineage.
    """
    
    __abstract__ = True
    
    # Audit columns for data lineage
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        comment="When record was created in silver layer"
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now(),
        comment="When record was last updated"
    )
