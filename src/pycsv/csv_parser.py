"""CSV parsing with automatic type inference."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime


@dataclass
class ParsedCSV:
    """Represents a parsed CSV file with inferred schema."""

    columns: list[Column]
    rows: list[dict]
    column_info: dict[str, str]  # column_name -> inferred type name


def infer_sqlalchemy_type(dtype: str):
    """Map pandas dtype to SQLAlchemy column type."""
    dtype_str = str(dtype)

    if dtype_str.startswith("int"):
        return Integer
    elif dtype_str.startswith("float"):
        return Float
    elif dtype_str.startswith("datetime"):
        return DateTime
    elif dtype_str == "bool":
        return Boolean
    else:
        return String


def parse_csv(file_path: Path) -> ParsedCSV:
    """Parse a CSV file and infer column types.

    Args:
        file_path: Path to the CSV file.

    Returns:
        ParsedCSV with inferred schema and data rows.
    """
    df = pd.read_csv(file_path)

    # Convert NaN to None for database compatibility
    df = df.where(pd.notnull(df), None)

    columns = []
    column_info = {}

    for col_name in df.columns:
        dtype = df[col_name].dtype
        sa_type = infer_sqlalchemy_type(dtype)
        column_info[col_name] = sa_type.__name__

        # Use String with length for text columns
        if sa_type == String:
            max_len = df[col_name].astype(str).str.len().max()
            col = Column(col_name, String(max(255, int(max_len * 1.5) if pd.notna(max_len) else 255)))
        else:
            col = Column(col_name, sa_type())

        columns.append(col)

    rows = df.to_dict(orient="records")

    return ParsedCSV(columns=columns, rows=rows, column_info=column_info)
