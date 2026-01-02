"""Gold layer base model."""
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class GoldBase(DeclarativeBase):
    """
    Base class for all Gold layer models.
    
    Gold layer contains business-ready, analytics-optimized data.
    Uses Star Schema design with dimension and fact tables.
    """
    
    __abstract__ = True
    
    # Audit column for tracking
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        comment="When record was created in gold layer"
    )
