"""Unit tests for configuration."""
import pytest
from pathlib import Path

from app.shared.config import Settings


class TestSettings:
    """Test Settings configuration."""

    def test_default_settings(self):
        """Test default configuration values."""
        settings = Settings()
        
        assert settings.postgres_db == "mimic_db"
        assert settings.postgres_port == 5432
        assert settings.batch_size == 1000
        assert settings.env == "development"

    def test_database_url(self):
        """Test database URL construction."""
        settings = Settings(
            postgres_user="test_user",
            postgres_password="test_pass",
            postgres_host="localhost",
            postgres_port=5432,
            postgres_db="test_db",
        )
        
        url = settings.database_url
        assert "test_user" in url
        assert "test_pass" in url
        assert "localhost" in url
        assert "test_db" in url
        assert "postgresql+psycopg2" in url

    def test_is_production(self):
        """Test production environment detection."""
        dev_settings = Settings(env="development")
        assert dev_settings.is_production is False
        
        prod_settings = Settings(env="production")
        assert prod_settings.is_production is True

    def test_csv_path_validation(self):
        """Test CSV path is converted to Path object."""
        settings = Settings(csv_data_path="./test_data")
        
        assert isinstance(settings.csv_data_path, Path)
        assert str(settings.csv_data_path) == "test_data"
