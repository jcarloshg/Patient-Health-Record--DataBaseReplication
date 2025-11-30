"""PostgreSQL database connection module using SQLAlchemy.

This module provides a configured database engine with connection pooling
and environment-based configuration.
"""

import os
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in the backend directory
env_path = Path(__file__).resolve().parents[5] / '.env'
load_dotenv(dotenv_path=env_path)


class DatabaseConfig:
    """Database configuration with validation and defaults."""

    def __init__(self):
        self.user = self._get_env_var('POSTGRES_USER', 'admin')
        self.password = self._get_env_var('POSTGRES_PASSWORD', '123456')
        self.database = self._get_env_var(
            'POSTGRES_DB', 'db_patient_health_record')
        self.host = self._get_env_var('POSTGRES_HOST', 'localhost')
        self.port = self._get_env_var('POSTGRES_PORT', '5432')

        # Connection pool settings
        self.pool_size = int(self._get_env_var('DB_POOL_SIZE', '5'))
        self.max_overflow = int(self._get_env_var('DB_MAX_OVERFLOW', '10'))
        self.pool_timeout = int(self._get_env_var('DB_POOL_TIMEOUT', '30'))
        self.pool_recycle = int(self._get_env_var('DB_POOL_RECYCLE', '3600'))

    @staticmethod
    def _get_env_var(key: str, default: str) -> str:
        """Get environment variable with fallback to default value."""
        value = os.getenv(key)
        if value is None:
            return default
        return value

    def get_database_url(self) -> str:
        """Build PostgreSQL connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


def create_db_engine(config: Optional[DatabaseConfig] = None) -> Engine:
    """Create and configure SQLAlchemy engine with connection pooling.

    Args:
        config: Optional DatabaseConfig instance. If None, creates from env vars.

    Returns:
        Configured SQLAlchemy Engine instance.
    """
    if config is None:
        config = DatabaseConfig()

    database_url = config.get_database_url()

    engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=config.pool_size,
        max_overflow=config.max_overflow,
        pool_timeout=config.pool_timeout,
        pool_recycle=config.pool_recycle,
        pool_pre_ping=True,  # Verify connections before using them
        echo=True,  # Set to True for SQL query logging during development
    )

    return engine


# Global engine instance
config = DatabaseConfig()
connection_engine = create_db_engine(config)
