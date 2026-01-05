"""Core import logic for CSV to PostgreSQL."""

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import Column

from .csv_parser import ParsedCSV, parse_csv
from .db import get_engine, create_table_from_schema, insert_rows


@dataclass
class ImportResult:
    """Result of a CSV import operation."""

    table_name: str
    rows_imported: int
    columns: list[str]
    column_types: dict[str, str]


def import_csv(
    file_path: Path,
    connection_string: str,
    table_name: str | None = None,
) -> ImportResult:
    """Import a CSV file into PostgreSQL.

    Args:
        file_path: Path to the CSV file.
        connection_string: PostgreSQL connection string.
        table_name: Target table name. Defaults to CSV filename without extension.

    Returns:
        ImportResult with details about the import.
    """
    if table_name is None:
        table_name = file_path.stem

    # Parse CSV and infer schema
    parsed = parse_csv(file_path)

    # Connect and create table
    engine = get_engine(connection_string)
    table = create_table_from_schema(engine, table_name, parsed.columns)

    # Insert data
    rows_imported = insert_rows(engine, table, parsed.rows)

    return ImportResult(
        table_name=table_name,
        rows_imported=rows_imported,
        columns=[col.name for col in parsed.columns],
        column_types=parsed.column_info,
    )


def preview_schema(file_path: Path) -> ParsedCSV:
    """Preview the inferred schema for a CSV file without importing.

    Args:
        file_path: Path to the CSV file.

    Returns:
        ParsedCSV with inferred schema information.
    """
    return parse_csv(file_path)
