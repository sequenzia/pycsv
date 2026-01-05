"""YAML configuration file support for database settings."""

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote_plus

import yaml


CONFIG_PATH = Path.home() / ".pycsv" / "config.yaml"


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


def load_config() -> DatabaseConfig | None:
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
