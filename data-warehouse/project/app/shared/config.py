"""Configuration management using Pydantic Settings."""
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database Configuration
    postgres_user: str = Field(default="mimic_user", description="PostgreSQL username")
    postgres_password: str = Field(default="mimic_password", description="PostgreSQL password")
    postgres_db: str = Field(default="mimic_db", description="PostgreSQL database name")
    postgres_host: str = Field(default="localhost", description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")

    # Connection Pool Settings
    db_pool_size: int = Field(default=10, description="Database connection pool size")
    db_max_overflow: int = Field(default=20, description="Max overflow connections")
    db_pool_recycle: int = Field(default=3600, description="Connection recycle time in seconds")

    # Application Settings
    env: str = Field(default="development", description="Environment (development/production)")
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="logs/app.log", description="Log file path")

    # Data Configuration
    csv_data_path: Path = Field(default=Path("./dataset"), description="Path to CSV data files")
    batch_size: int = Field(default=1000, description="Batch size for data loading")

    @field_validator("csv_data_path", mode="before")
    @classmethod
    def validate_csv_path(cls, v):
        """Convert string path to Path object."""
        return Path(v) if isinstance(v, str) else v

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL database URL."""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.env.lower() == "production"


# Global settings instance
settings = Settings()
