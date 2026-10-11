# Ingestion

This directory contains the Python components responsible for ingesting raw marketing campaign data into the DuckDB warehouse.

## Responsibilities

- Load source CSV files from `data/raw/`.
- Inspect and validate input data.
- Load the data into the DuckDB raw schema.
- Support source-to-warehouse reconciliation and ingestion verification.

## Pipeline Flow

```text
data/raw/*.csv
       ↓
Python Ingestion
       ↓
DuckDB Raw Layer
       ↓
dbt Transformations
       ↓
Analytical Marts
       ↓
PostgreSQL
```

Python handles ingestion and initial validation, while dbt and SQL handle downstream transformations and analytical modeling.

