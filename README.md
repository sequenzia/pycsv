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

### Using environment variables

```bash
export PYCSV_DATABASE_URL=postgresql://user:pass@localhost/mydb
pycsv import data.csv --table users
```

Or use individual env vars:

```bash
export PYCSV_DB_HOST=localhost
export PYCSV_DB_PORT=5432
export PYCSV_DB_USER=postgres
export PYCSV_DB_PASSWORD=secret
export PYCSV_DB_DATABASE=mydb
pycsv import data.csv --table users
```

### Using a .env file

Create `.env` in your working directory:

```
PYCSV_DB_HOST=localhost
PYCSV_DB_PORT=5432
PYCSV_DB_USER=postgres
PYCSV_DB_PASSWORD=secret
PYCSV_DB_DATABASE=mydb
```

### Using a YAML config file

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
2. `PYCSV_DATABASE_URL` environment variable (full connection string)
3. `PYCSV_DB_*` environment variables or `.env` file
4. `~/.pycsv/config.yaml` config file

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
