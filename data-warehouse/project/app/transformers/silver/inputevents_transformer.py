"""Input events transformer: Bronze → Silver (unified CV + MV)."""
from typing import Dict, Any, Optional, Generator, List
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.bronze import BronzeInputEventsCareVue, BronzeInputEventsMetaVision
from app.models.silver import SilverInputEvent
from app.shared import logger


class InputEventsTransformer:
    """
    Transform input events from Bronze to Silver layer.
    
    Merges CareVue and MetaVision data into a single unified table.
    """
    
    def __init__(self, session: Session, batch_size: int = 1000):
        self.session = session
        self.batch_size = batch_size
        self.stats = {"total": 0, "transformed": 0, "errors": 0}
    
    @property
    def silver_model(self):
        return SilverInputEvent
    
    def calculate_duration(self, start: datetime, end: datetime) -> Optional[float]:
        """Calculate duration in hours."""
        if not start or not end:
            return None
        delta = end - start
        return round(delta.total_seconds() / 3600, 2)
    
    def transform_cv_record(self, bronze: BronzeInputEventsCareVue) -> Dict[str, Any]:
        """Transform CareVue record."""
        return {
            "row_id": bronze.row_id,
            "subject_id": bronze.subject_id,
            "hadm_id": bronze.hadm_id,
            "icustay_id": bronze.icustay_id,
            "source_system": "CareVue",
            "itemid": bronze.itemid,
            "charttime": bronze.charttime,
            "starttime": None,
            "endtime": None,
            "amount": bronze.amount,
            "amountuom": bronze.amountuom,
            "rate": bronze.rate,
            "rateuom": bronze.rateuom,
            "cgid": bronze.cgid,
            "duration_hours": None,
            "is_bolus": bronze.rate is None or bronze.rate == 0,
        }
    
    def transform_mv_record(self, bronze: BronzeInputEventsMetaVision) -> Dict[str, Any]:
        """Transform MetaVision record."""
        duration = self.calculate_duration(bronze.starttime, bronze.endtime)
        
        return {
            "row_id": bronze.row_id + 1000000,  # Offset to avoid ID conflicts
            "subject_id": bronze.subject_id,
            "hadm_id": bronze.hadm_id,
            "icustay_id": bronze.icustay_id,
            "source_system": "MetaVision",
            "itemid": bronze.itemid,
            "charttime": bronze.starttime,
            "starttime": bronze.starttime,
            "endtime": bronze.endtime,
            "amount": bronze.amount,
            "amountuom": bronze.amountuom,
            "rate": bronze.rate,
            "rateuom": bronze.rateuom,
            "cgid": bronze.cgid,
            "duration_hours": duration,
            "is_bolus": bronze.orderid is None,
        }
    
    def read_batches(self) -> Generator[List[Dict[str, Any]], None, None]:
        """Read and transform both CV and MV records."""
        # Process CareVue
        offset = 0
        while True:
            batch = (
                self.session.query(BronzeInputEventsCareVue)
                .offset(offset)
                .limit(self.batch_size)
                .all()
            )
            if not batch:
                break
            
            transformed = []
            for record in batch:
                self.stats["total"] += 1
                try:
                    transformed.append(self.transform_cv_record(record))
                    self.stats["transformed"] += 1
                except Exception as e:
                    self.stats["errors"] += 1
                    logger.warning(f"Error transforming CV record: {e}")
            
            yield transformed
            offset += self.batch_size
        
        # Process MetaVision
        offset = 0
        while True:
            batch = (
                self.session.query(BronzeInputEventsMetaVision)
                .offset(offset)
                .limit(self.batch_size)
                .all()
            )
            if not batch:
                break
            
            transformed = []
            for record in batch:
                self.stats["total"] += 1
                try:
                    transformed.append(self.transform_mv_record(record))
                    self.stats["transformed"] += 1
                except Exception as e:
                    self.stats["errors"] += 1
                    logger.warning(f"Error transforming MV record: {e}")
            
            yield transformed
            offset += self.batch_size
    
    def write_batch(self, silver_data: List[Dict[str, Any]]):
        """Write transformed data to silver table."""
        for data in silver_data:
            silver_record = self.silver_model(**data)
            self.session.merge(silver_record)
        self.session.commit()
    
    def transform(self):
        """Execute full transformation."""
        logger.info("Starting Bronze → Silver transformation for inputevents (CV + MV)")
        
        for batch in self.read_batches():
            if batch:
                self.write_batch(batch)
        
        logger.info(
            f"Transformation complete for inputevents: "
            f"{self.stats['transformed']}/{self.stats['total']} records "
            f"({self.stats['errors']} errors)"
        )
        
        return self.stats
