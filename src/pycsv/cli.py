"""CLI entry point using Typer."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from .config import load_config, CONFIG_PATH
from .db import test_connection
from .importer import import_csv, preview_schema

app = typer.Typer(help="Import CSV files into PostgreSQL.")


@app.command("import")
def import_command(
    csv_file: Annotated[Path, typer.Argument(help="Path to the CSV file to import")],
    table: Annotated[
        Optional[str],
        typer.Option("--table", "-t", help="Target table name (default: CSV filename)"),
    ] = None,
    db: Annotated[
        Optional[str],
        typer.Option(
            "--db",
            "-d",
            envvar="PYCSV_DATABASE_URL",
            help="PostgreSQL connection string (or set PYCSV_DATABASE_URL)",
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Preview inferred schema without importing"),
    ] = False,
) -> None:
    """Import a CSV file into PostgreSQL."""
    if not csv_file.exists():
        typer.echo(f"Error: File not found: {csv_file}", err=True)
        raise typer.Exit(1)

    if dry_run:
        parsed = preview_schema(csv_file)
        typer.echo(f"Inferred schema for: {csv_file.name}")
        typer.echo("-" * 40)
        for col_name, col_type in parsed.column_info.items():
            typer.echo(f"  {col_name}: {col_type}")
        typer.echo("-" * 40)
        typer.echo(f"Total rows: {len(parsed.rows)}")
        return

    if not db:
        # Try loading from config file
        config = load_config()
        if config:
            db = config.to_connection_string()
        else:
            typer.echo(
                f"Error: Database connection required. Use --db, set PYCSV_DATABASE_URL, or create {CONFIG_PATH}",
                err=True,
            )
            raise typer.Exit(1)

    try:
        result = import_csv(csv_file, db, table)
        typer.echo(f"Successfully imported {result.rows_imported} rows into '{result.table_name}'")
        typer.echo(f"Columns: {', '.join(result.columns)}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command("test")
def test_command(
    db: Annotated[
        Optional[str],
        typer.Option(
            "--db",
            "-d",
            envvar="PYCSV_DATABASE_URL",
            help="PostgreSQL connection string (or set PYCSV_DATABASE_URL)",
        ),
    ] = None,
) -> None:
    """Test the database connection."""
    if not db:
        config = load_config()
        if config:
            db = config.to_connection_string()
        else:
            typer.echo(
                f"Error: Database connection required. Use --db, set PYCSV_DATABASE_URL, or create {CONFIG_PATH}",
                err=True,
            )
            raise typer.Exit(1)

    typer.echo("Testing connection...")
    success, message = test_connection(db)

    if success:
        typer.echo(f"Connection successful: {message}")
    else:
        typer.echo(f"Connection failed: {message}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
