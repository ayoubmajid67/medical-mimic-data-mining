"""Gold layer dimension: Service."""
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import GoldBase


class DimService(GoldBase):
    """
    Service dimension table.
    
    Contains medical service definitions.
    """
    
    __tablename__ = "dim_service"
    __table_args__ = {"schema": "gold"}
    
    # Surrogate key
    service_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Natural key
    curr_service: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    
    # Attributes
    service_description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    def __repr__(self) -> str:
        return f"<DimService(service_key={self.service_key}, curr_service={self.curr_service})>"
