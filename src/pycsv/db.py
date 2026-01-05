"""Database connection and table management using SQLAlchemy."""

from sqlalchemy import create_engine, text, MetaData, Table, Column
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def get_engine(connection_string: str) -> Engine:
    """Create a SQLAlchemy engine from a connection string."""
    return create_engine(connection_string)


def test_connection(connection_string: str) -> tuple[bool, str]:
    """Test database connection.

    Returns:
        Tuple of (success, message).
    """
    try:
        engine = get_engine(connection_string)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
        return True, f"PostgreSQL {version}"
    except Exception as e:
        return False, str(e)


def create_table_from_schema(
    engine: Engine,
    table_name: str,
    columns: list[Column],
) -> Table:
    """Create a table dynamically from a list of SQLAlchemy columns."""
    metadata = MetaData()
    table = Table(table_name, metadata, *columns)
    metadata.create_all(engine)
    return table


def insert_rows(engine: Engine, table: Table, rows: list[dict]) -> int:
    """Insert rows into a table. Returns the number of rows inserted."""
    with Session(engine) as session:
        session.execute(table.insert(), rows)
        session.commit()
    return len(rows)
