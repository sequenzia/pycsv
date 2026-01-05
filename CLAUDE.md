# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pyCSV is a CLI tool to import CSV files into PostgreSQL with automatic schema detection. It uses SQLAlchemy for database operations, Typer for CLI, and Pandas for type inference.

## Development Commands

```bash
# Install in development mode
uv pip install -e .

# Run the CLI
pycsv import <csv_file> --table <table_name> --db <connection_string>

# Preview schema without importing
pycsv import <csv_file> --dry-run
```

## Architecture

```
src/pycsv/
├── cli.py          # Typer CLI entry point, handles args and dry-run
├── config.py       # YAML config loading from ~/.pycsv/config.yaml
├── csv_parser.py   # Pandas-based CSV parsing with dtype→SQLAlchemy type mapping
├── db.py           # SQLAlchemy engine, dynamic table creation, bulk insert
└── importer.py     # Orchestrates parsing and import, returns ImportResult
```

**Data flow**: `cli.py` → `importer.py` → `csv_parser.py` + `db.py`

**Config priority**: CLI flag > env var (`PYCSV_DATABASE_URL`) > config file (`~/.pycsv/config.yaml`)

The `ParsedCSV` dataclass carries inferred columns and row data between modules. Type inference maps pandas dtypes (int64, float64, object, datetime64, bool) to SQLAlchemy types (Integer, Float, String, DateTime, Boolean).
