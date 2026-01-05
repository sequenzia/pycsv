"""Configuration support for database settings via YAML, env vars, and .env file."""

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote_plus

import yaml
from dotenv import load_dotenv


CONFIG_PATH = Path.home() / ".pycsv" / "config.yaml"

# Environment variable names
ENV_DB_HOST = "PYCSV_DB_HOST"
ENV_DB_PORT = "PYCSV_DB_PORT"
ENV_DB_USER = "PYCSV_DB_USER"
ENV_DB_PASSWORD = "PYCSV_DB_PASSWORD"
ENV_DB_DATABASE = "PYCSV_DB_DATABASE"


@dataclass
class DatabaseConfig:
    """Database connection configuration."""

    host: str
    port: int
    user: str
    password: str
    database: str

    def to_connection_string(self) -> str:
        """Build PostgreSQL connection string from config fields."""
        password_encoded = quote_plus(self.password)
        return f"postgresql://{self.user}:{password_encoded}@{self.host}:{self.port}/{self.database}"


def load_from_env() -> DatabaseConfig | None:
    """Load database configuration from environment variables.

    Looks for .env file in current directory first, then checks env vars.

    Returns:
        DatabaseConfig if all required env vars are set, None otherwise.
    """
    # Load .env file if it exists
    load_dotenv()

    user = os.getenv(ENV_DB_USER)
    password = os.getenv(ENV_DB_PASSWORD)
    database = os.getenv(ENV_DB_DATABASE)

    # Required fields
    if not all([user, password, database]):
        return None

    return DatabaseConfig(
        host=os.getenv(ENV_DB_HOST, "localhost"),
        port=int(os.getenv(ENV_DB_PORT, "5432")),
        user=user,
        password=password,
        database=database,
    )


def load_from_yaml() -> DatabaseConfig | None:
    """Load database configuration from ~/.pycsv/config.yaml.

    Returns:
        DatabaseConfig if config file exists and is valid, None otherwise.
    """
    if not CONFIG_PATH.exists():
        return None

    try:
        with open(CONFIG_PATH) as f:
            data = yaml.safe_load(f)

        if not data or "database" not in data:
            return None

        db = data["database"]
        return DatabaseConfig(
            host=db.get("host", "localhost"),
            port=int(db.get("port", 5432)),
            user=db["user"],
            password=db["password"],
            database=db["database"],
        )
    except (yaml.YAMLError, KeyError, TypeError, ValueError):
        return None


def load_config() -> DatabaseConfig | None:
    """Load database configuration with priority: env vars/.env > YAML config.

    Returns:
        DatabaseConfig if configuration is found, None otherwise.
    """
    # Try env vars / .env first
    config = load_from_env()
    if config:
        return config

    # Fall back to YAML config
    return load_from_yaml()
