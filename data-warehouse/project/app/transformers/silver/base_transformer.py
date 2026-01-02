"""Base transformer for Bronze to Silver layer."""
from abc import ABC, abstractmethod
from typing import Generator, List, Dict, Any

from sqlalchemy.orm import Session

from app.shared import logger


class BaseSilverTransformer(ABC):
    """
    Abstract base class for Bronze to Silver transformations.
    
    Provides common functionality for:
    - Reading from bronze tables
    - Applying transformations
    - Writing to silver tables
    - Error handling and logging
    """
    
    def __init__(self, session: Session, batch_size: int = 1000):
        """
        Initialize transformer.
        
        Args:
            session: SQLAlchemy session
            batch_size: Number of rows per batch
        """
        self.session = session
        self.batch_size = batch_size
        self.stats = {"total": 0, "transformed": 0, "errors": 0}
    
    @property
    @abstractmethod
    def bronze_model(self):
        """Bronze model class to read from."""
        pass
    
    @property
    @abstractmethod
    def silver_model(self):
        """Silver model class to write to."""
        pass
    
    @abstractmethod
    def transform_record(self, bronze_record) -> Dict[str, Any]:
        """
        Transform a single bronze record to silver format.
        
        Args:
            bronze_record: SQLAlchemy model instance from bronze
            
        Returns:
            Dictionary of silver field values
        """
        pass
    
    def read_bronze_batches(self) -> Generator[List, None, None]:
        """
        Read bronze records in batches.
        
        Yields:
            Batches of bronze records
        """
        offset = 0
        while True:
            batch = (
                self.session.query(self.bronze_model)
                .offset(offset)
                .limit(self.batch_size)
                .all()
            )
            
            if not batch:
                break
                
            yield batch
            offset += self.batch_size
    
    def transform_batch(self, bronze_batch: List) -> List[Dict[str, Any]]:
        """
        Transform a batch of bronze records.
        
        Args:
            bronze_batch: List of bronze records
            
        Returns:
            List of transformed dictionaries
        """
        transformed = []
        
        for record in bronze_batch:
            self.stats["total"] += 1
            try:
                silver_data = self.transform_record(record)
                if silver_data:
                    transformed.append(silver_data)
                    self.stats["transformed"] += 1
            except Exception as e:
                self.stats["errors"] += 1
                logger.warning(f"Error transforming record: {e}")
        
        return transformed
    
    def write_silver_batch(self, silver_data: List[Dict[str, Any]]):
        """
        Write transformed data to silver table using bulk insert.
        
        Args:
            silver_data: List of transformed dictionaries
        """
        from sqlalchemy.dialects.postgresql import insert
        
        if not silver_data:
            return
        
        # Use bulk insert with upsert (ON CONFLICT DO UPDATE)
        stmt = insert(self.silver_model).values(silver_data)
        
        # Get primary key column name
        pk_columns = [c.name for c in self.silver_model.__table__.primary_key.columns]
        
        # Create update dict for all non-pk columns
        update_dict = {
            c.name: stmt.excluded[c.name] 
            for c in self.silver_model.__table__.columns 
            if c.name not in pk_columns
        }
        
        # Upsert: insert or update on conflict
        stmt = stmt.on_conflict_do_update(
            index_elements=pk_columns,
            set_=update_dict
        )
        
        self.session.execute(stmt)
        self.session.commit()
    
    def transform(self):
        """Execute full transformation process."""
        silver_name = self.silver_model.__tablename__
        logger.info(f"Starting Bronze → Silver transformation for {silver_name}")
        
        for batch in self.read_bronze_batches():
            silver_data = self.transform_batch(batch)
            if silver_data:
                self.write_silver_batch(silver_data)
            logger.debug(f"Processed batch: {len(batch)} records")
        
        logger.info(
            f"Transformation complete for {silver_name}: "
            f"{self.stats['transformed']}/{self.stats['total']} records "
            f"({self.stats['errors']} errors)"
        )
        
        return self.stats
