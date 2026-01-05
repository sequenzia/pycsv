# pyCSV

CLI tool to import CSV files into PostgreSQL with automatic schema detection.

## Installation

```bash
uv pip install -e .
```

## Usage

### Import a CSV file

```bash
pycsv import data.csv --table users --db postgresql://user:pass@localhost/mydb
```

### Preview inferred schema (dry run)

```bash
pycsv import data.csv --dry-run
```

### Using environment variable for database connection

```bash
export PYCSV_DATABASE_URL=postgresql://user:pass@localhost/mydb
pycsv import data.csv --table users
```

### Using a config file

Create `~/.pycsv/config.yaml`:

```yaml
database:
  host: localhost
  port: 5432
  user: postgres
  password: secret
  database: mydb
```

Then run without specifying connection:

```bash
pycsv import data.csv --table users
```

## Connection Priority

1. `--db` command line flag
2. `PYCSV_DATABASE_URL` environment variable
3. `~/.pycsv/config.yaml` config file

## Options

- `--table, -t`: Target table name (defaults to CSV filename)
- `--db, -d`: PostgreSQL connection string (or set `PYCSV_DATABASE_URL`)
- `--dry-run`: Preview inferred schema without importing

## Type Inference

pyCSV automatically infers column types from your CSV data:

| CSV Data Type | PostgreSQL Type |
|---------------|-----------------|
| Integer       | INTEGER         |
| Float         | FLOAT           |
| DateTime      | TIMESTAMP       |
| Boolean       | BOOLEAN         |
| Text          | VARCHAR         |
