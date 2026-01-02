"""Test configuration and fixtures."""
import pytest
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_csv_row():
    """Sample CSV row data."""
    return {
        "row_id": "1",
        "subject_id": "10001",
        "gender": "M",
        "dob": "1980-01-01 00:00:00",
        "expire_flag": "0",
    }


@pytest.fixture
def sample_field_mapping():
    """Sample field type mapping."""
    return {
        "row_id": "int",
        "subject_id": "int",
        "gender": "str",
        "dob": "datetime",
        "expire_flag": "bool",
    }


@pytest.fixture
def temp_csv_file(tmp_path):
    """Create a temporary CSV file for testing."""
    csv_file = tmp_path / "test.csv"
    csv_content = """subject_id,gender,dob,expire_flag
10001,M,1980-01-01 00:00:00,0
10002,F,1985-05-15 00:00:00,1
"""
    csv_file.write_text(csv_content)
    return csv_file
