"""Unit tests for CSV loader."""
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

from app.transformers.bronze.base_loader import BaseCSVLoader
from app.models.bronze import BronzePatients


class TestBaseCSVLoader:
    """Test BaseCSVLoader functionality."""

    def test_parse_value_int(self):
        """Test parsing integer values."""
        loader = BaseCSVLoader(BronzePatients, Path("dummy.csv"))
        
        assert loader.parse_value("123", "int") == 123
        assert loader.parse_value("", "int") is None
        assert loader.parse_value("  ", "int") is None

    def test_parse_value_float(self):
        """Test parsing float values."""
        loader = BaseCSVLoader(BronzePatients, Path("dummy.csv"))
        
        assert loader.parse_value("123.45", "float") == 123.45
        assert loader.parse_value("", "float") is None

    def test_parse_value_bool(self):
        """Test parsing boolean values."""
        loader = BaseCSVLoader(BronzePatients, Path("dummy.csv"))
        
        assert loader.parse_value("1", "bool") is True
        assert loader.parse_value("0", "bool") is False
        assert loader.parse_value("true", "bool") is True
        assert loader.parse_value("", "bool") is None

    def test_parse_value_datetime(self):
        """Test parsing datetime values."""
        loader = BaseCSVLoader(BronzePatients, Path("dummy.csv"))
        
        result = loader.parse_value("2020-01-01 12:30:00", "datetime")
        assert isinstance(result, datetime)
        assert result.year == 2020
        assert result.month == 1
        assert result.day == 1

    def test_parse_value_string(self):
        """Test parsing string values."""
        loader = BaseCSVLoader(BronzePatients, Path("dummy.csv"))
        
        assert loader.parse_value("test", "str") == "test"
        assert loader.parse_value("  test  ", "str") == "test"
        assert loader.parse_value("", "str") is None

    def test_transform_row(self):
        """Test row transformation."""
        loader = BaseCSVLoader(BronzePatients, Path("dummy.csv"))
        
        row = {
            "subject_id": "10001",
            "gender": "M",
            "expire_flag": "0",
        }
        
        field_mapping = {
            "subject_id": "int",
            "gender": "str",
            "expire_flag": "bool",
        }
        
        result = loader.transform_row(row, field_mapping)
        
        assert result["subject_id"] == 10001
        assert result["gender"] == "M"
        assert result["expire_flag"] is False

    def test_get_stats(self):
        """Test statistics retrieval."""
        loader = BaseCSVLoader(BronzePatients, Path("dummy.csv"))
        
        stats = loader.get_stats()
        assert "total" in stats
        assert "loaded" in stats
        assert "errors" in stats
        assert stats["total"] == 0
