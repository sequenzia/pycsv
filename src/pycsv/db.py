"""Database connection and table management using SQLAlchemy."""

from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def get_engine(connection_string: str) -> Engine:
    """Create a SQLAlchemy engine from a connection string."""
    return create_engine(connection_string)


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
