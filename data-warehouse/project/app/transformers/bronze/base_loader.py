"""Base loader for CSV data ingestion."""
import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List, Optional, Type

from sqlalchemy.orm import Session

from app.shared import logger


class BaseCSVLoader:
    """
    Generic CSV loader with batch processing and error handling.
    
    Provides common functionality for loading CSV files into Bronze tables.
    """

    def __init__(
        self,
        model_class: Type,
        csv_path: Path,
        batch_size: int = 1000,
        skip_errors: bool = True,
    ):
        """
        Initialize CSV loader.

        Args:
            model_class: SQLAlchemy model class
            csv_path: Path to CSV file
            batch_size: Number of rows per batch
            skip_errors: Whether to skip rows with errors
        """
        self.model_class = model_class
        self.csv_path = csv_path
        self.batch_size = batch_size
        self.skip_errors = skip_errors
        self.stats = {"total": 0, "loaded": 0, "errors": 0}

    def parse_value(self, value: str, field_type: str) -> Any:
        """
        Parse CSV string value to appropriate Python type.

        Args:
            value: String value from CSV
            field_type: Expected field type

        Returns:
            Parsed value or None
        """
        # Handle empty strings
        if not value or value.strip() == "":
            return None

        try:
            if field_type == "int":
                return int(value)
            elif field_type == "float":
                return float(value)
            elif field_type == "bool":
                return value.strip() in ("1", "true", "True", "TRUE")
            elif field_type == "datetime":
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            elif field_type == "date":
                return datetime.strptime(value, "%Y-%m-%d").date()
            else:  # string
                return value.strip()
        except (ValueError, TypeError) as e:
            logger.warning(f"Failed to parse value '{value}' as {field_type}: {e}")
            return None

    def transform_row(self, row: Dict[str, str], field_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Transform CSV row to model-compatible dictionary.

        Args:
            row: Raw CSV row (strings)
            field_mapping: Map of field_name -> field_type

        Returns:
            Transformed row dict
        """
        transformed = {}
        for field_name, field_type in field_mapping.items():
            if field_name in row:
                transformed[field_name] = self.parse_value(row[field_name], field_type)
        return transformed

    def read_csv_batches(
        self, field_mapping: Dict[str, str]
    ) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Read CSV file in batches.

        Args:
            field_mapping: Map of field_name -> field_type

        Yields:
            Batches of transformed rows
        """
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        logger.info(f"Reading CSV: {self.csv_path}")

        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            batch = []

            for row in reader:
                self.stats["total"] += 1

                try:
                    transformed = self.transform_row(row, field_mapping)
                    batch.append(transformed)

                    if len(batch) >= self.batch_size:
                        yield batch
                        batch = []

                except Exception as e:
                    self.stats["errors"] += 1
                    if self.skip_errors:
                        logger.warning(f"Error transforming row {self.stats['total']}: {e}")
                        continue
                    else:
                        raise

            # Yield remaining rows
            if batch:
                yield batch

    def load_batch(self, session: Session, batch: List[Dict[str, Any]]) -> int:
        """
        Load a batch of rows into database.

        Args:
            session: SQLAlchemy session
            batch: List of transformed row dicts

        Returns:
            Number of rows loaded
        """
        loaded = 0
        for row in batch:
            try:
                instance = self.model_class(**row)
                session.add(instance)
                loaded += 1
            except Exception as e:
                self.stats["errors"] += 1
                if self.skip_errors:
                    logger.warning(f"Error loading row: {e}")
                    session.rollback()
                    continue
                else:
                    raise

        try:
            session.commit()
            self.stats["loaded"] += loaded
            return loaded
        except Exception as e:
            session.rollback()
            logger.error(f"Batch commit failed: {e}")
            raise

    def load(self, session: Session, field_mapping: Dict[str, str]):
        """
        Execute full CSV load process.

        Args:
            session: SQLAlchemy session
            field_mapping: Map of field_name -> field_type
        """
        logger.info(f"Starting load for {self.model_class.__tablename__}")
        start_time = datetime.now()

        try:
            for batch in self.read_csv_batches(field_mapping):
                loaded = self.load_batch(session, batch)
                logger.debug(f"Loaded batch: {loaded} rows")

            duration = (datetime.now() - start_time).total_seconds()
            logger.info(
                f"Load complete for {self.model_class.__tablename__}: "
                f"{self.stats['loaded']}/{self.stats['total']} rows in {duration:.2f}s "
                f"({self.stats['errors']} errors)"
            )

        except Exception as e:
            logger.error(f"Load failed for {self.model_class.__tablename__}: {e}")
            raise

    def get_stats(self) -> Dict[str, int]:
        """Get loading statistics."""
        return self.stats.copy()
